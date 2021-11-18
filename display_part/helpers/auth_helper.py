import msal
import os
import time

from site_package.my_module import create_logger
from icecream import ic
ic.configureOutput(prefix='', includeContext=True)
# ic.disable()
# set_level = '' # 全てに影響
set_level = 'debug'
# set_level = 'info'
logger = create_logger(__name__, set_level=set_level)


def load_cache(request):
    # Check for a token cache in the session
    cache = msal.SerializableTokenCache()
    if request.session.get('token_cache'):
        cache.deserialize(request.session['token_cache'])

    return cache


def save_cache(request, cache):
    # If cache has changed, persist back to session
    if cache.has_state_changed:
        request.session['token_cache'] = cache.serialize()


def get_msal_app(cache=None):
    # Initialize the MSAL confidential client
    auth_app = msal.ConfidentialClientApplication(
        os.environ['app_id'],
        authority=os.environ['authority'],
        client_credential=os.environ['app_secret'],
        token_cache=cache)

    return auth_app

# Method to generate a sign-in flow


def get_sign_in_flow():
    auth_app = get_msal_app()

    return auth_app.initiate_auth_code_flow(
        os.environ["scopes"].split(','),
        redirect_uri=os.environ['redirect'])

# Method to exchange auth code for access token


def get_token_from_code(request):
    cache = load_cache(request)
    auth_app = get_msal_app(cache)

    # Get the flow saved in session
    flow = request.session.pop('auth_flow', {})

    result = auth_app.acquire_token_by_auth_code_flow(flow, request.GET)
    save_cache(request, cache)

    return result


def store_user(request, user):
    try:
        request.session['user'] = {
            'is_authenticated': True,
            'name': user.get('displayName') or '',
            'email': user['mail'] if (user['mail'] != None) else user['userPrincipalName'],
            'timeZone': user['mailboxSettings'].get('timeZone') if user['mailboxSettings'].get('timeZone') != None else 'UTC'
        }
    except Exception as e:
        logger.error(f'{type(e)} {e}')


def get_token(request):
    cache = load_cache(request)
    auth_app = get_msal_app(cache)
    # auth_app = get_msal_app(None)

    accounts = auth_app.get_accounts()
    if accounts:
        result = auth_app.acquire_token_silent(
            os.environ["scopes"].split(','),
            account=accounts[0])

        save_cache(request, cache)

        return result['access_token']


def remove_user_and_token(request):
    if 'token_cache' in request.session:
        del request.session['token_cache']

    if 'user' in request.session:
        del request.session['user']

    if 'manager' in request.session:
        del request.session['manager']

    if 'super' in request.session:
        del request.session['super']
