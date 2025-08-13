from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

import os
import sys
import glob
import shutil
import time
from time import sleep

from download_wait import download_file
from selenium_click import element_click

# カレントディレクトリの取得
current_dir = os.getcwd()

LOGIN_ID = 'himihiromu@icloud.com'
PASSWORD = 'himihiromu0104'
TEMP_DOWNLOAD_DIR = r'E:\hiromu\同人\tempDownloadFile'
DOWNLOAD_COMPLETE_DIR = r'E:\hiromu\同人\fanza'


def get_chrome_service():

    # 一時ダウンロードフォルダパスの設定
    tmp_download_dir = TEMP_DOWNLOAD_DIR

    # 一時フォルダが存在していたら消す(前回のが残存しているかも)
    if os.path.isdir(tmp_download_dir):
        shutil.rmtree(tmp_download_dir)

    # 一時ダウンロードフォルダの作成
    os.mkdir(tmp_download_dir)

    # ドライバのパス設定
    driver_path = r'E:\web_driver\chromedriver-win64\chromedriver-win64\chromedriver.exe'

    # ブラウザパス
    browser_path = r'E:\web_driver\chrome-win64\chrome-win64\chrome.exe'

    # Chromeオプション設定でダウンロード先を変更
    options = webdriver.ChromeOptions()
    prefs = {
        'download.default_directory': tmp_download_dir,
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False,
        'profile.default_content_setting_values.notifications': 2,
    }
    options.add_experimental_option('prefs', prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.binary_location = browser_path

    return Service(executable_path=driver_path), options


def dmm_login(driver, dmm_url, login_id, password):
    driver.get(dmm_url)

    login_id_input = driver.find_element(By.ID, 'login_id')
    login_id_input.send_keys(login_id)

    login_password_input = driver.find_element(By.ID, 'password')
    login_password_input.send_keys(password)

    login_button = driver.find_element(By.XPATH, '//*[@id="loginbutton_script_on"]/span/input')
    element_click(driver, login_button)


def get_item_element_list(driver, dmm_mylibrary_url):
    driver.get(dmm_mylibrary_url)

    movie_ul = driver.find_element(By.CLASS_NAME, 'purchasedListArea1Znew').find_elements(By.CLASS_NAME, 'localListProduct1pSCw')

    return movie_ul


def check_age_click(driver):
    sleep(2)
    cur_url = driver.current_url
    if cur_url.startswith('https://www.dmm.co.jp/age_check/'):

        age_check_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div/div[2]/a')
        element_click(driver, age_check_button)
        return True

    return False


def is_item_exists(title, download_file_path):
    download_file_name = map(lambda x: x.split('\\')[-1], glob.glob(f'{download_file_path}\\*.*'))
    for fn in download_file_name:
        if fn.startswith(title):
            return True
    return False


def main():
    service, options = get_chrome_service()

    # オプションを適用してChromeを起動
    driver = webdriver.Chrome(service=service, options=options)

    # === 画面遷移 ===
    dmm_login(driver, 'https://accounts.dmm.co.jp/service/login/password/', LOGIN_ID, PASSWORD)

    if check_age_click(driver):
        sleep(2)

    element_total = 0
    loop_complete = False

    while True:
        download_element_list = get_item_element_list(
            driver,
            'https://www.dmm.co.jp/dc/-/mylibrary/'
        )
        print(download_element_list)
        print(len(download_element_list))


        for el in download_element_list[0:]:
            image = el.find_element(By.CLASS_NAME, 'listLeft3OY39')
            element_click(driver, image)
            sleep(3)
            title_path = driver.find_element(By.CLASS_NAME, 'productDetailTitleN0PbV').text
            title_path = title_path.replace("/", " ")
            print(title_path)
            if is_item_exists(title_path, DOWNLOAD_COMPLETE_DIR):
                continue
            if driver.find_element(By.XPATH, f'//*[@id="js-mylibraryFolderTop"]/div/div[1]/div[2]/div/div/div/div[1]/a').text == 'アプリで見る':
                continue
            download_file_path = download_file(driver, TEMP_DOWNLOAD_DIR, DOWNLOAD_COMPLETE_DIR, f'//*[@id="js-mylibraryFolderTop"]/div/div[1]/div[2]/div/div/div/div[1]/a')
            root_ext_pair = os.path.splitext(download_file_path)
            os.rename(download_file_path, DOWNLOAD_COMPLETE_DIR + '\\' + title_path + root_ext_pair[1])
            sleep(2)
        if element_total == len(download_element_list):
            break
        else:
            element_total = len(download_element_list)

    # === ダウンロード完了後処理 ===
    # Chromeを閉じる
    driver.quit()


if __name__ == '__main__':
    main()

