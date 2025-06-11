import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


#r = requests.get('https://shopee.com.my/Mobile-Accessories-cat.11000979')
#print(r.status_code)
options = Options()
options.browser_version = 'stable'
options.page_load_strategy = 'eager'
#options.add_argument('--headless')  # run in background
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-logging")
options.add_argument("--log-level=3")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-webrtc")
driver = webdriver.Chrome(options=options)

url = 'https://shopee.com.my/Mobile-Accessories-cat.11000979'
driver.set_window_size(1300, 800)
driver.get(url)
time.sleep(5) 

language = driver.find_element(by = By.CSS_SELECTOR, value="button")
language.click
time.sleep(5) 
driver.save_screenshot("ss.png")
driver.quit
'''soup = BeautifulSoup(, 'html.parser')
print(r.text)
product_list = soup.find_all("link")#, classmethod='shopee-search-item-result__item')
#print(product_list)
product_data = []

for product in product_list:
    product_chars = {
        'product_name' : product.find('a', class_='contents')['href'],
        'product_link' : product.find('a', class_='contents')['href']       
    }
    product_data.append(product_chars)

csv_file = 'shopee_product_data.csv'

with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['product_name', 'product_link'])
    writer.writeheader()
    for row in product_data:
        writer.writerow(row)

print("File Loaded into excel")'''
    
