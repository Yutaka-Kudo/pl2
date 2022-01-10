from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from openpyxl import Workbook

import time
import functools
from io import BytesIO
import tempfile
import os
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import json

from config import settings
from daily_report.actions.recording_helper import RecordingHelper
from daily_report.actions.graph_helper import get_user, search_path, find_item_in_folder, get_file, put_file, generate_path, match_stores_by_email, URIAGE_FOLDER_ID, select_filename
from display_part.helpers.auth_helper import get_token
from display_part.views import create_df_by_paytype
from . import models
from upload_part import models as uploadPartModels

from dotenv import load_dotenv

from site_package.my_module import create_logger
from icecream import ic
ic.configureOutput(prefix='', includeContext=True)
# ic.disable()
# set_level = '' # 全てに影響
set_level = 'debug'
# set_level = 'info'
logger = create_logger(__name__, set_level=set_level)

load_dotenv()

# test_name = '売上月報'
test_name = 'テスト用'

permit_over_hour = 6


cell_info = {
    'col_of_kumisuu_at_first': 6,
    'row_of_lunch_free': 14,
    'delivery_top_row': 29,
    'labor_top_row': 46,
    'cost_top_row': 48,
    'total_salary': 'b46',

    'food_top_row': 6,
    'drink_top_row': 19,
    'cash_shiire_row': 25,
    'cash_shoumou_row': 26,
    'other_row': 36,
    'other_detail_row': 38,

    'col_of_salesPage_first': 2,
    'row_of_salesPage_first': 8,
}


def get_time():  # 時刻を外に出してグローバルだとサーバー上で更新されない
    if os.getenv("TZ") == 'Asia/Tokyo':
        to_day = (datetime.now() - relativedelta(hours=permit_over_hour)).date()
        now = datetime.now()
    else:  # heroku上の時間に注意
        to_day = (datetime.now() + relativedelta(hours=(9-permit_over_hour))).date()
        now = datetime.now()
    return to_day, now


def home(request):
    to_day, now = get_time()
    context = initialize_context(request)
    context['to_day'] = to_day
    context['now'] = now
    context['permit_over_hour'] = permit_over_hour
    if context['user'].get('email'):
        _, store_name = match_stores_by_email(context['user']['email'])
        context['store_name'] = store_name

    context['debug'] = request.session.get('debug', 'false')

    return render(request, 'daily_report/home.html', context)


def initialize_context(request):
    context = {}

    # Check for any errors in the session
    error = request.session.pop('flash_error', None)

    if error is None:
        context['errors'] = []
        context['errors'].append(error)

    # Check for user in the session
    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context


def get_request(request):
    to_day, _ = get_time()
    if settings.DEBUG:
        # デバッグ用ーーーーーーーーーーー
        request.session['debug_date'] = request.GET.get('debug_date')
        debug_date = int(request.GET.get('debug_date'))
        to_day += relativedelta(day=debug_date)
        ic(to_day)
        # デバッグ用ーーーーーーーーーーー

    to_day = datetime.strftime(to_day, '%Y-%m-%d')

    def create_inputedCost_dict(request):
        inputed_costs = {'food': [], 'drink': [], 'other': []}
        i = 1
        while request.GET.get(f'food{i}') is not None:
            inputed_costs['food'].append(request.GET.get(f'food{i}') or '0')
            i += 1
        i = 1
        while request.GET.get(f'drink{i}') is not None:
            inputed_costs['drink'].append(request.GET.get(f'drink{i}') or '0')
            i += 1
        i = 1
        while request.GET.get(f'other{i}') is not None:
            inputed_costs['other'].append(request.GET.get(f'other{i}') or '0')
            i += 1
        return inputed_costs
    inputed_costs = create_inputedCost_dict(request)

    email = request.session['user']['email']

    # デバッグ用ーーーーーーーーーーー
    if settings.DEBUG:
        which_store = request.GET.get('which_store')
        if which_store == 'fes':
            email = os.environ['MS_ID']
        elif which_store == 'garage':
            email = 'garage@gmail.com'
        elif which_store == 'toro':
            email = 'toro@gmail.com'
        elif which_store == 'wana':
            email = 'wana@gmail.com'
        elif which_store == 'nakame':
            email = 'nakame@gmail.com'
    # デバッグ用ーーーーーーーーーーー

    context = dict(to_day=to_day, email=email, inputed_costs=inputed_costs)
    context['what'] = 'for_record'
    return render(request, 'daily_report/progress_index.html', {'initial_data': json.dumps(context), 'what': 'for_record'})


def recording(make_progress_func, token, initial_data):
    ic(initial_data)
    email = initial_data['email']
    to_day = datetime.strptime(initial_data['to_day'], '%Y-%m-%d').date()

    # for iii in range(1, 27):
    #     to_day = datetime(2021, 10, iii).date()

    logger.info(f'to_day: {to_day}')

    # メールアドレスで店舗を照合
    store_name, name_for_file = match_stores_by_email(email)

    # file_nameを決める。オリジナルか複製かーーーーーーー
    target_file_name = select_filename(name_for_file, store_name, to_day, test_name, models)

    ic(target_file_name)
    # ーーーーーーーfile_nameを決める。オリジナルか複製か

    make_progress_func()

    # 入力用インスタンス生成
    rcdhlp = RecordingHelper(to_day, store_name)

    make_progress_func()
    # 人件費取得ーーーーーーーーーーーーーーーー
    rcdhlp.get_df_labor()
    rcdhlp.calculate_total_labor()

    make_progress_func()
    make_progress_func()

    # 売上取得ーーーーーーーーーーーーーーーー
    rcdhlp.get_sales()

    make_progress_func()

    which = {
        'store': target_file_name.split('】')[0].replace('【', ''),
        'year': target_file_name.split('】')[1][:4],
        'file_name': target_file_name,
    }
    ic(which)

    result_obj = {}

    target_path, store_folder_id, year_folder_id = search_path(token, which)

    if not target_path:  # 見つからなかったら終了
        if not store_folder_id:
            logger.error(f'not find store folder → {which["store"]}')
            result_obj['msg'] = err_msg_template(f'{which["store"]} 店舗フォルダ')
            result_obj['judge'] = 'error'
            return result_obj
        else:
            logger.error(f'not find year folder → {which["year"]}')
            result_obj['msg'] = err_msg_template(f'{which["year"]}フォルダ')
            result_obj['judge'] = 'error'
            return result_obj

    logger.debug('search path OK!!')
    ic(target_path)

    make_progress_func()

    target_file_response = get_file(token, target_path)
    if target_file_response.status_code == 404:
        # 変な時間設定でアイテムが見つからない場合のエラー処理
        logger.error(f"{target_file_response.json()['error']['message']}\n{target_file_response.json()['error']['innerError']['date']}Z")
        result_obj['msg'] = f"{err_msg_template(f'{target_file_name}')}"
        result_obj['judge'] = 'error'
        return result_obj

    target_file_binary = target_file_response.content
    target_file_binary = BytesIO(target_file_binary)  # 変換
    logger.debug('get file OK!!')

    make_progress_func()

    target_file: Workbook = rcdhlp.record_in_file(target_file_binary, cell_info, initial_data['inputed_costs'])
    # テスト用
    # target_file: Workbook = rcdhlp.record_in_file(target_file_binary, cell_info, initial_data['inputed_costs'], test=True)

    make_progress_func()
    make_progress_func()

    # workbookをバイナリに戻す
    with tempfile.NamedTemporaryFile() as tmp:
        target_file.save(tmp.name)
        virtual_wb = BytesIO(tmp.read())

    res = put_file(token, target_path, virtual_wb)
    virtual_wb.close()

    logger.info(res)

    # ファイル開かれてる時
    if res.status_code == 423:
        basename_without_ext = os.path.splitext(target_file_name)[0]
        if '_複製' not in basename_without_ext:
            instead_file_name = target_file_name.replace(basename_without_ext, basename_without_ext + '_複製1')
        else:
            copy_count: str = basename_without_ext.split('_複製')[1]
            counter = 1
            while True:  # 一応、複製ファイルの上書きがないように。いらないか
                instead_file_name = target_file_name.replace('_複製' + copy_count, '_複製' + str(int(copy_count) + counter))
                if not find_item_in_folder(token, year_folder_id, instead_file_name):
                    break
                counter += 1

        models.TargetFileName.objects.update_or_create(store=store_name, defaults={'file_name': instead_file_name})
        instead_path = generate_path(year_folder_id, instead_file_name)
        # workbookをバイナリに戻す
        with tempfile.NamedTemporaryFile() as tmp:
            target_file.save(tmp.name)
            virtual_wb = BytesIO(tmp.read())
        res = put_file(token, instead_path, virtual_wb)
        virtual_wb.close()

        logger.info(f'元のファイルが開かれているため、複製を作り新しいファイル名で保存しました。update models.TargetFileName add suffix: {instead_file_name}')
        result_obj['msg'] = f'元のファイルが開かれているため、複製を作り新しいファイル名で保存しました。\n以降はこちらを使用します: {instead_file_name}'
        result_obj['judge'] = 'success'
        return result_obj

    make_progress_func()

    result_obj['msg'] = f'{target_file_name} {to_day}日分 \n日報に書き込みできました。\nお疲れさまでした。'
    result_obj['judge'] = 'success'
    return result_obj


def get_request_for_create(request):
    email = request.session['user']['email']
    context = dict(email=email)
    context['what'] = 'for_create'
    return render(request, 'daily_report/progress_index.html', {'initial_data': json.dumps(context), 'what': 'for_create'})


def create_next_file(make_progress_func, token, initial_data):
    result_obj = {}

    to_day, _ = get_time()

    # to_day = datetime(2021, 12, 5)

    # メールアドレスで店舗を照合
    email = initial_data['email']
    store_name, name_for_file = match_stores_by_email(email)

    target_file_name = f'【{name_for_file}】{to_day.year}{str(to_day.month).zfill(2)}{test_name}.xlsx'
    ic(target_file_name)
    which = {
        'store': target_file_name.split('】')[0].replace('【', ''),
        'year': target_file_name.split('】')[1][:4],
        'file_name': target_file_name,
    }

    target_path, store_folder_id, year_folder_id = search_path(token, which)
    if not target_path:
        if not store_folder_id:
            logger.error(f'not find store folder → {which["store"]}')
            result_obj['msg'] = err_msg_template(f'{which["store"]} 店舗フォルダ')
            result_obj['judge'] = 'error'
            return result_obj

    make_progress_func()

    messages = []

    if to_day.month == 1:  # 対象が1月のとき
        year_folder_id, result_y = create_yearFolder(token, store_folder_id, to_day.year)
        messages.append(f'「{to_day.year}」フォルダを作成しました。' if result_y else '')
    make_progress_func()
    make_progress_func()
    result_f = create_newFile(token, to_day, year_folder_id, email, None)
    make_progress_func()
    make_progress_func()
    if result_f[0] == 1:
        messages.append(f'{result_f[1]}は、すでに存在します。')
    if result_f[0] == 2:
        messages.append(f'「{to_day.year}年{to_day.month}月」のファイルを作成しました。' if result_f[0] else '')
    elif result_f[0] == 3:
        result_obj['msg'] = err_msg_template(f"{result_f[1]}\nフォーマットファイル")
        result_obj['judge'] = 'error'
        return result_obj

    to_day = to_day + relativedelta(months=1)

    if to_day.month == 1:  # 対象が1月のとき
        year_folder_id, result_y = create_yearFolder(token, store_folder_id, to_day.year)
        messages.append(f'「{to_day.year}」フォルダを作成しました。' if result_y else '')
    make_progress_func()
    make_progress_func()
    result_f = create_newFile(token, to_day, year_folder_id, email, None)
    make_progress_func()
    make_progress_func()
    if result_f[0] == 1:
        messages.append(f'{result_f[1]}は、すでに存在します。')
    elif result_f[0] == 2:
        messages.append(f'「{to_day.year}年{to_day.month}月」のファイルを作成しました。' if result_f[0] else '')
    elif result_f[0] == 3:
        result_obj['msg'] = err_msg_template(f"{result_f[1]}\nフォーマットファイル")
        result_obj['judge'] = 'error'
        return result_obj
    make_progress_func()

    result_obj['msg'] = '\n'.join(messages)
    result_obj['judge'] = 'success'
    return result_obj


def create_yearFolder(token, store_folder_id, creating_name):
    creating_name = str(creating_name)
    # あるなら中止
    finded_result = find_item_in_folder(token, store_folder_id, creating_name)
    if finded_result:
        logger.info(f'{creating_name} は既にありました。')
        return finded_result['id'], None

    store_folder_path = generate_path(store_folder_id)
    folder_item = {"name": creating_name, "folder": {}}
    ic(creating_name)

    # フォルダ作成
    res = put_file(token, store_folder_path, folder_item, request_type='post')
    if res.status_code >= 300:
        raise Exception(f'ステータスコード:{res.status_code}\nレスポンスヘッダ:{res.json()}')
    logger.debug(f'フォルダ作成: {creating_name}')

    new_year_folder_id = res.json()['id']
    return new_year_folder_id, True


def create_newFile(token, date_to_create, year_folder_id, email, rcdhlp=None):
    store_name, name_for_file = match_stores_by_email(email)
    date_to_create = date_to_create + relativedelta(day=1)  # 初期化 1日にする
    new_file_name = f'【{name_for_file}】{date_to_create.year}{str(date_to_create.month).zfill(2)}{test_name}.xlsx'

    # あるなら中止
    if find_item_in_folder(token, year_folder_id, new_file_name):
        logger.info(f'{new_file_name}は、すでに存在します。')
        return 1, new_file_name

    format_file_name = f'【{name_for_file}】売上月報フォーマット.xlsx'
    ic(format_file_name)
    which = {
        'store': format_file_name.split('】')[0].replace('【', ''),
        # 'year': format_file_name.split('】')[1][:4],
        'file_name': format_file_name,
    }

    format_file_path = search_path(token, which, where='format_file')
    target_file_response = get_file(token, format_file_path)
    if target_file_response.status_code >= 300:  # 常にあるはず。なければエラー
        logger.critical(f'not find formatFile: {which["file_name"]}')
        return 3, format_file_name

    target_file_binary = target_file_response.content
    target_file_binary = BytesIO(target_file_binary)  # 変換

    new_month_date = f'{date_to_create.year}/{date_to_create.month}/{date_to_create.day}'
    if not rcdhlp:
        to_day, _ = get_time()  # 時間はなんでもいいか？今の所
        rcdhlp = RecordingHelper(to_day, store_name)
    new_file: Workbook = rcdhlp.replace_month_cell(target_file_binary, new_month_date)
    logger.debug('replace month')

    # workbookをバイナリに戻す
    with tempfile.NamedTemporaryFile() as tmp:
        new_file.save(tmp.name)
        virtual_wb = BytesIO(tmp.read())
    logger.debug('workbookをバイナリに戻す')

    target_path = generate_path(year_folder_id, new_file_name)
    logger.debug('create new path')

    result = put_file(token, target_path, virtual_wb)
    logger.debug(result)
    logger.info(f'新しいファイルを作成しました。{new_file_name}')

    return 2, 'create'


def err_msg_template(finded_item_str):
    return f'{finded_item_str} が見つかりません。\n\n<b>考えられる原因</b>\n・削除されている\n・名前が変更されている\n・他のフォルダに移動されている\n→ 見つからない場合は管理者に問い合わせてください。\n\n・月が変わり新しいファイルが作成されていない \n→ ブラウザを戻って『来月のファイルを作成』ボタンを押してください。'


def setup(request):
    """進捗管理インスタンスを作成する"""
    progress = models.Progress.objects.create()
    return HttpResponse(progress.pk)


def show_progress(request):
    """DBから進捗データを持ってくる"""
    if "progress_pk" in request.GET:
        progress_pk = request.GET.get("progress_pk")
        progress = get_object_or_404(models.Progress, pk=progress_pk)
        persent = str(int(progress.now / progress.total * 100)) + "%"
        return render(request, "daily_report/progress_bar.html", {"persent": persent})
    else:
        return HttpResponse("エラー")


def make_progress(pk):
    """引数のプライマリーキーに紐づく進捗を進める"""
    progress = get_object_or_404(models.Progress, pk=pk)
    progress.now += 10
    progress.save()


def set_hikisuu(pk):
    """引数を固定する"""
    return functools.partial(make_progress, pk=pk)


def recording_bg(request):
    """時間のかかる関数を実行する"""
    initial_data = json.loads(request.GET.get("initial_data"))
    token = get_token(request)
    if "progress_pk" in request.GET:
        # progress_pkが指定されている場合の処理
        progress_pk = request.GET.get("progress_pk")
        result = recording(set_hikisuu(progress_pk), token, initial_data)
        progress = get_object_or_404(models.Progress, pk=progress_pk)
        progress.delete()
        return render(request, "daily_report/progress_result.html", {"msg": result['msg'], 'judge': result['judge']})
    else:
        # progress_pkが指定されていない場合の処理
        return HttpResponse("エラー")


def create_next_file_bg(request):
    """時間のかかる関数を実行する"""
    initial_data = json.loads(request.GET.get("initial_data"))
    token = get_token(request)
    if "progress_pk" in request.GET:
        # progress_pkが指定されている場合の処理
        progress_pk = request.GET.get("progress_pk")
        result = create_next_file(set_hikisuu(progress_pk), token, initial_data)
        progress = get_object_or_404(models.Progress, pk=progress_pk)
        progress.delete()
        return render(request, "daily_report/progress_result.html", {"msg": result['msg'], 'judge': result['judge']})
    else:
        # progress_pkが指定されていない場合の処理
        return HttpResponse("エラー")
