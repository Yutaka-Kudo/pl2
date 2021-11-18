from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


import os
from time import sleep
import glob
import datetime

from site_package.my_module import create_logger
from site_package.browsing_sub import set_options, Wait_located, capture
from icecream import ic
ic.configureOutput(prefix='', includeContext=True)
# ic.disable()
# set_level = 'debug'
set_level = 'info'
logger = create_logger(__name__, set_level=set_level)




def DL_labor_and_put_csv(tmpdir_name, store_name, to_day, headless: bool = True):
    options = webdriver.ChromeOptions()
    options = set_options(options, headless=headless)
    # options = set_options(options, headless=False)

    # 一時ディレクトリを保存先に。
    options.add_experimental_option("prefs", {
        "download.default_directory": tmpdir_name,
    })

    driver = webdriver.Chrome('chromedriver', options=options)
    dw = Wait_located(driver)

    driver.get('https://app.recoru.in/')
    logger.debug('ページ表示')
    driver.find_element_by_id('contractId').send_keys(os.environ['RECORU_CONTRACT_ID'])
    driver.find_element_by_id('authId').send_keys(os.environ['RECORU_AUTH_ID'])
    driver.find_element_by_id('password').send_keys(os.environ['RECORU_PW'] + Keys.ENTER)

    logger.info('recoruログイン')

    store_name = 'FES' if store_name == 'fes' else 'Garage' if store_name == 'garage' else '路地ノ裏　灯篭' if store_name == 'tourou' else '焼ジビエ　罠一目' if store_name == 'wanaichi' else '焼ジビエ　罠　中目黒' if store_name == 'wananakame' else ''
    dw.wait_lacated_xpath(f'//span[text()="{store_name}"]').click()
    sleep(2)

    logger.debug(f'店舗選択OK {store_name}')

    # 日にち調整ーーーーーーーーーーーーー
    def get_recoru_date() -> datetime.date:
        recoru_date = driver.find_element_by_xpath('//div[@id="DIV-DATE"]//label').text.split('(')[0]  # ex.'2021年10月5日(火)'
        recoru_date = datetime.datetime.strptime(recoru_date, '%Y年%m月%d日').date()
        return recoru_date
    recoru_date = get_recoru_date()
    while recoru_date != to_day:
        logger.debug(f"recoru_date {recoru_date}")
        if recoru_date < to_day:
            driver.find_element_by_xpath('//div[@id="DIV-DATE"]/a[contains(text(),"翌日へ")]').click()
        if recoru_date > to_day:
            driver.find_element_by_xpath('//div[@id="DIV-DATE"]/a[contains(text(),"前日へ")]').click()
        sleep(.75)
        recoru_date = get_recoru_date()
    logger.info(f"finally_recoru_date {recoru_date}")
    # 日にち調整ーーーーーーーーーーーーー
    sleep(2)

    driver.find_element_by_xpath('//input[@value="ファイル出力"]').click()
    logger.debug('ファイル出力クリック')
    # sleep(3)
    # driver.find_element_by_xpath('//label[@for="targetLayoutId3"]').click()
    dw.wait_lacated_xpath('//label[@for="targetLayoutId3"]').click()
    logger.debug('targetLayoutId3クリック')
    driver.find_element_by_id('DOWNLOAD-BTN').click()
    logger.debug('downloadボタンクリック')

    def wait_file_download(specified_dir):
        """Google Chromeでダウンロードを開始すると「*.crdownload」ファイルが生成される。完了するとそのファイルは削除される仕組"""
        # 待機タイムアウト時間(秒)設定
        timeout_second = 10
        # 指定時間分待機
        for _ in range(timeout_second):
            # ファイル一覧取得
            match_file_path = os.path.join(specified_dir, '*.*')
            files = glob.glob(match_file_path)

            if files:
                # ファイル名の拡張子に、'.crdownload'が含むかを確認
                extensions = [file_name for file_name in files if '.crdownload' in os.path.splitext(file_name)]

                # '.crdownload'が見つからなかったら終了
                if not extensions:
                    break

            # 一秒待つ
            sleep(1)
        else:
            # 指定時間待っても .crdownload 以外のファイルが確認できない場合 エラー
            raise Exception('Csv file cannot be finished downloading!')

        return

    wait_file_download(tmpdir_name)
    driver.quit()
    logger.info('download完了')
