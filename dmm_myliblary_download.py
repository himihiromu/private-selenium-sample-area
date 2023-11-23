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
TEMP_DOWNLOAD_DIR = r'E:\hiromu\動画\tempDownloadFile'
DOWNLOAD_COMPLETE_DIR = r'E:\hiromu\動画\fanza'


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


def get_movie_element_list(driver, dmm_mylibrary_url):
    driver.get(dmm_mylibrary_url)

    movie_ul = driver.find_element(By.ID, 'js-list').find_element(By.CLASS_NAME, 'mySearchPictList')

    return movie_ul.find_elements(By.CLASS_NAME, 'mySearchList_item')


def check_age_click(driver):
    sleep(2)
    cur_url = driver.current_url
    if cur_url.startswith('https://www.dmm.co.jp/age_check/'):

        age_check_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div/div[2]/a')
        element_click(driver, age_check_button)
        return True

    return False


def is_movie_exists(title, download_file_path):
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

    download_element_list = get_movie_element_list(
        driver,
        'https://www.dmm.co.jp/digital/-/mylibrary/search/'
    )

    for el in download_element_list[0:]:
        image = el.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "p")
        element_click(driver, image)
        sleep(3)
        title = driver.find_element(By.ID, 'js-product-tabs').find_element(By.CLASS_NAME, 'title').find_element(By.TAG_NAME, 'cite').text
        download_list = driver.find_elements(By.XPATH, '//*[@id="js-product-tabs"]/div[3]/div[1]/div[2]/div[2]/div/div[2]/div/ul[1]/li')
        for i, dl in enumerate(download_list):
            if len(download_list) == 1:
                soe = ''
                title_path = title + '.dcv'
            else:
                soe = '[' + str(i + 1) + ']'
                title_path = title + str(i + 1) + '.dcv'
            title_path = title_path.replace("/", " ")
            print(title_path)
            if is_movie_exists(title_path, DOWNLOAD_COMPLETE_DIR):
                continue
            download_file_path = download_file(driver, TEMP_DOWNLOAD_DIR, DOWNLOAD_COMPLETE_DIR, f'//*[@id="js-product-tabs"]/div[3]/div[1]/div[2]/div[2]/div/div[2]/div/ul[1]/li{soe}/span/a')
            os.rename(download_file_path, DOWNLOAD_COMPLETE_DIR + '\\' + title_path)
        close_button = driver.find_element(By.ID, 'js-detail-close')
        element_click(driver, close_button)
        sleep(2)

    # === ダウンロード完了後処理 ===
    # Chromeを閉じる
    driver.quit()


if __name__ == '__main__':
    main()

