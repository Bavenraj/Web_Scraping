import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import time

#r = requests.get('https://shopee.com.my/Mobile-Accessories-cat.11000979')
#print(r.status_code)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # run in background
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)

url = 'https://shopee.com.my/Mobile-Accessories-cat.11000979'
driver.get(url)

#time.sleep(5) 

soup = BeautifulSoup(driver.page_source, 'html.parser')
product_list = soup.findAll('li', class_='shopee-search-item-result__item')
print(product_list)
product_data = []

for product in product_list:
    product_chars = {
        'product_name' : product.find('img')['alt'],
        'product_link' : product.find('a', class_='contents')['href']       
    }
    product_data.append(product_chars)

csv_file = 'shopee_product_data.csv'

with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['product_name', 'product_link'])
    writer.writeheader()
    for row in product_data:
        writer.writerow(row)

print("File Loaded into excel")
    
