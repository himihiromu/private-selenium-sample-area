from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def get_chrome_service():

    # ブラウザパス
    browser_path = r'E:\web_driver\chrome-win64\chrome-win64\chrome.exe'

    # Chromeオプション設定でダウンロード先を変更
    options = webdriver.ChromeOptions()
    prefs = {
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False,
        'profile.default_content_setting_values.notifications': 2,
    }
    options.add_experimental_option('prefs', prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    return Service(executable_path=ChromeDriverManager().install()), options

service, options = get_chrome_service()

    # オプションを適用してChromeを起動
driver = webdriver.Chrome(service=service, options=options)

# Booking.comの検索ページ
url = "https://www.booking.com/searchresults.html?ss=Tokyo"
driver.get(url)

# ページが完全に読み込まれるまで待機（必要に応じて調整）
time.sleep(5)

# ホテル情報を取得
hotels = []
hotel_elements = driver.find_elements(By.CLASS_NAME, "sr_property_block_main_row")

for element in hotel_elements:
    try:
        name = element.find_element(By.CLASS_NAME, "sr-hotel__name").text.strip()
        address = element.find_element(By.CLASS_NAME, "bui-u-sr-only").text.strip()
        link = element.find_element(By.CLASS_NAME, "hotel_name_link").get_attribute("href").strip()
        hotels.append({
            "name": name,
            "address": address,
            "url": link
        })
    except Exception as e:
        print(f"Error: {e}")

# 結果を表示
for hotel in hotels:
    print(hotel)

# ドライバーを閉じる
driver.quit()
