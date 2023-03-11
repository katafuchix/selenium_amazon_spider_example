from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re

# linux
#options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
#driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Mac
driver = webdriver.Chrome(ChromeDriverManager().install())

url = "https://www.amazon.co.jp/-/en/KADOKAWA/dp/B0BV5GPZPQ/ref=sr_1_2?keywords=%E3%82%B0%E3%83%A9%E3%83%93%E3%82%A2&qid=1678506342&sr=8-2"
url = "https://www.amazon.co.jp/-/en/%E6%A8%B9%E6%99%BA%E5%AD%90-ebook/dp/B0BXF2Y3F2/ref=sr_1_6?keywords=%E3%82%B0%E3%83%A9%E3%83%93%E3%82%A2&qid=1678506342&sr=8-6"
url = "https://www.amazon.co.jp/-/en/%E4%BC%8A%E7%B9%94-%E3%82%82%E3%81%88/dp/4768317162/ref=sr_1_4?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&keywords=%E3%82%B0%E3%83%A9%E3%83%93%E3%82%A2&qid=1678506990&sr=8-4"
url = "https://www.amazon.co.jp/-/en/%E9%87%91%E5%AD%90%E6%99%BA%E7%BE%8E/dp/B0BX1XV1YY/ref=sr_1_2?crid=2VYTILWJRLKSU&amp;keywords=%E9%87%91%E5%AD%90%E6%99%BA%E7%BE%8E&amp;qid=1678510695&amp;sprefix=%E9%87%91%E5%AD%90%E6%99%BA%E7%BE%8E%2Caps%2C163&amp;sr=8-2"
url = "https://www.amazon.co.jp/-/jp/%E4%BC%8A%E7%B9%94-%E3%82%82%E3%81%88/dp/4768317162/ref=sr_1_4?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&keywords=%E3%82%B0%E3%83%A9%E3%83%93%E3%82%A2&qid=1678506990&sr=8-4&language=ja_JP"

try:
    driver.get(url)
    time.sleep(1)
    try:
        title_element = driver.find_element(By.ID, 'productTitle')
    except Exception as e:
        # 年齢認証がある場合
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR, ".a-button-inner")
            links = [a.get_attribute("href") for a in buttons[0].find_elements(By.TAG_NAME, "a")]
            print(links)
            driver.get(links[0])
            time.sleep(1)
        except Exception as e:
            print(e)

    result = dict()
    result["site"] = "Amazon"
    result["url"] = driver.current_url
    result["asin"] = driver.current_url.split("/")[-2]
    title_element = driver.find_element(By.ID, 'productTitle')
    result["title"] = title_element.text

    item_price = 0
    elem = driver.find_element(By.ID, "tmmSwatches")
    # 通常価格検索
    spans = elem.find_elements(By.TAG_NAME, 'span.a-color-base')
    for span in spans:
        try:
            child_spans = span.find_elements(By.TAG_NAME, 'span.a-size-base, span.a-color-price')
            for child_span in child_spans:
                try:
                    price = re.sub(r"\D", "", child_span.text)
                    if price != None and len(price) >= 3:
                        item_price = price
                        break
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    # 上記で価格が取得できない場合
    if item_price == 0:
        spans = elem.find_elements(By.TAG_NAME, 'span.a-color-secondary')
        for span in spans:
            try:
                child_spans = span.find_elements(By.TAG_NAME, 'span.a-color-secondary')
                for child_span in child_spans:
                    try:
                        price = re.sub(r"\D", "", child_span.text)
                        if price != None and len(price) >= 3:
                            item_price = price
                            break
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)

    # 上記２つでも価格が取得できない場合
    if item_price == 0:
        try:
            value = driver.find_element(By.ID, "youPayValue")
            print(value)
            price = re.sub(r"\D", "", value.text)
            print(price)
            if price != None and len(price) >= 3:
                item_price = price
        except Exception as e:
            print(e)

    result["price"] = item_price

    # 結果の確認
    print(result)
except Exception as e:
    print(e)
finally:
    driver.quit()
