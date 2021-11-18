from __future__ import annotations
from datetime import date
from io import BytesIO
import requests
import os

from site_package.my_module import create_logger
from icecream import ic

from dotenv import load_dotenv
load_dotenv()

ic.configureOutput(prefix='', includeContext=True)
# ic.disable()
# set_level = '' # 全てに影響
set_level = 'debug'
# set_level = 'info'
logger = create_logger(__name__, set_level=set_level)


GRAPH_URL = 'https://graph.microsoft.com/v1.0'

SHARED_DRIVE_ID = os.environ['SHARED_DRIVE_ID']
URIAGE_FOLDER_ID = os.environ['URIAGE_FOLDER_ID']


def get_user(token):
    # Send GET to /me
    user = requests.get(
        '{0}/me'.format(GRAPH_URL),
        headers={
            'Authorization': 'Bearer {0}'.format(token)
        },
        params={
            '$select': 'displayName,mail,mailboxSettings,userPrincipalName'
        })
    # Return the JSON result

    return user.json()


def match_stores_by_email(email):
    '''メールアドレスで店舗を照合'''
    if email == 'fes@gmail.com':
        store_name, name_for_file = 'fes', 'FES'
    elif email == 'garage@gmail.com':
        store_name, name_for_file = 'garage', 'Garage'
    elif email == 'tourou@gmail.com':
        store_name, name_for_file = 'tourou', '灯篭'
    elif email == 'wana@gmail.com':
        store_name, name_for_file = 'wanaichi', '罠一目'
    elif email == 'y_kudo@hotmail.com':
        store_name, name_for_file = 'fes', 'FES'
    else:
        raise Exception(f'アカウントが不正です。{email}')
    return store_name, name_for_file


def select_filename(name_for_file, store_name, to_day:date, test_name, models):
    # file_nameを決める。オリジナルか複製かーーーーーーー
    # OneDrive覗きに行くと時間かかるからDB管理で早く
    target_file_name = f'【{name_for_file}】{to_day.year}{str(to_day.month).zfill(2)}{test_name}.xlsx'
    filename_obj, created = models.TargetFileName.objects.get_or_create(store=store_name)
    if created:
        filename_obj.file_name = target_file_name
        filename_obj.save()
        logger.info(f'models.TargetFileName created new store: {store_name}')
    else:
        filename_obj_yearmonth = filename_obj.file_name.split('】')[1][:6]
        target_file_yearmonth = target_file_name.split('】')[1][:6]
        if filename_obj_yearmonth == target_file_yearmonth:
            # DBにあればそっち使う
            target_file_name = filename_obj.file_name
        else:
            # 月が変わったらきれいな名前にする
            filename_obj.file_name = target_file_name
            filename_obj.save()
            logger.info(f'clear models.TargetFileName suffix as new month: {to_day.year}{str(to_day.month).zfill(2)}')
    return target_file_name

def search_path(token, which, where: str = 'file'):
    store_folder = find_item_in_folder(token, URIAGE_FOLDER_ID, which['store'])
    if not store_folder:  # 常にあるはず。なければエラー
        logger.critical(f'not find storeFolder: {which["store"]}')
        return '', '', ''

    if where == 'format_file':
        target_path = generate_path(store_folder['id'], which['file_name'])
        return target_path

    year_folder = find_item_in_folder(token, store_folder['id'], which['year'])
    if not year_folder:  # 常にあるはず。なければエラー
        logger.info(f'not find storeFolder → {which["year"]}')
        return '', store_folder['id'], ''

    if where == 'file':
        target_path = generate_path(year_folder['id'], which['file_name'])
        return target_path, store_folder['id'], year_folder['id']


def generate_path(parent_id: str, file_name: str = '') -> str:
    if file_name:
        # get,put用  リクエストURLの末尾に「content」をつけてある。
        return f'{GRAPH_URL}/drives/{SHARED_DRIVE_ID}/items/{parent_id}:/{file_name}:/content'
    else:
        return f'{GRAPH_URL}/drives/{SHARED_DRIVE_ID}/items/{parent_id}/children'


def find_item_in_folder(token, folder_id, search: str, plural: bool = False):
    headers = {'Authorization': f'Bearer {token}'}
    folder_path: str = generate_path(folder_id)
    items_in_folder: list = requests.get(folder_path, headers=headers).json()['value']

    if plural:
        searched_results = [f for f in items_in_folder if search in f['name']]
        return searched_results

    searched_result = [f for f in items_in_folder if search == f['name']]
    if searched_result:
        return searched_result[0]
    else:
        return {}


def get_file(token, target_path):
    headers = {'Authorization': f'Bearer {token}'}
    res = requests.get(target_path, headers=headers)
    return res


def put_file(token, target_path, file, request_type: str = 'put'):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    if request_type == 'put':
        result = requests.put(target_path, headers=headers, data=file)
    else:
        headers['Content-Type'] = 'application/json'
        result = requests.post(target_path, headers=headers, json=file)
    return result
