from selenium import webdriver
from selenium.webdriver.common.by import By

import os
import sys
import glob
import shutil
import time

from selenium_click import element_click


def download_file(driver, download_dir_name, save_dir_name, download_button_xpath):
    # ダウンロード開始するリンクをクリック
    download_button = driver.find_element(By.XPATH, download_button_xpath)

    element_click(driver, download_button)

    time.sleep(2)

    # 待機タイムアウト時間(秒)設定
    timeout_second = 60 * 60 * 2

    # 指定時間分待機
    for i in range(timeout_second + 1):
        # ファイル一覧取得
        download_file_name = glob.glob(f'{download_dir_name}\\*.*')

        extension_list = list()

        # ファイルが存在する場合
        if download_file_name:
            for fn in download_file_name:

                # 拡張子の抽出
                extension = os.path.splitext(fn)
                extension_list.append(extension[1])

            # 拡張子が '.crdownload' ではない ダウンロード完了 待機を抜ける
            if ".crdownload" not in extension_list:
                print(extension_list)
                time.sleep(2)
                break

        # 指定時間待っても .crdownload 以外のファイルが確認できない場合 エラー
        if i >= timeout_second:
            # == エラー処理をここに記載 ==
            # 終了処理
            driver.quit()
            # 一時フォルダの削除
            shutil.rmtree(download_dir_name)
            sys.exit()

        # 一秒待つ
        time.sleep(2)
    return shutil.move(glob.glob(f'{download_dir_name}\\*.*')[0], save_dir_name)