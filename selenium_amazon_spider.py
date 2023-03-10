from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# linux
#options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
#driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Mac
driver = webdriver.Chrome(ChromeDriverManager().install())

keyword = "グラビア"
url = "https://www.amazon.co.jp/s?k={}".format(keyword)

driver.get(url)
time.sleep(3)

# 商品を取り出す
item_elements = driver.find_elements(By.CSS_SELECTOR, ".sg-col-4-of-24.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.s-widget-spacing-small.sg-col-4-of-20")

for elem in item_elements:
    # item url
    links = [a.get_attribute('href') for a in elem.find_elements(By.CSS_SELECTOR, ".a-link-normal.s-no-outline")]
    item_url = links[0]
    # asin
    asin = links[0].split("/")[-2]
    # item name
    alts = [a.get_attribute('alt') for a in elem.find_elements(By.TAG_NAME, "img")]
    item_name = alts[0]

    # images
    imgs = [a for a in elem.find_elements(By.TAG_NAME, "img")]
    images = {}
    try:
        srcsets =  imgs[0].get_attribute('srcset').split(',')
        images = { s.strip().split(' ')[1] : s.strip().split(' ')[0] for s in srcsets }
    except:
        images = {}

    print(item_name)
    print(asin)
    print(item_url)
    print(images)

    print("--------")
