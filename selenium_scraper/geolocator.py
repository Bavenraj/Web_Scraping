from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging
import time
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Initializing WebDriver")

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
driver.maximize_window()

logging.info("Loading Google Maps")
driver.get("https://www.google.com/maps/")
time.sleep(5)

logging.info("Getting input search box")
input = driver.find_element(by = By.CLASS_NAME, value = "searchboxinput")
input.clear()

logging.info("Searching for location")
input.send_keys("kfc selangor", Keys.ENTER)
time.sleep(5)

scrollableElement = driver.find_element(by=By.CSS_SELECTOR, value =".kA9KIf")
last_height = 0

while True:
    driver.execute_script('arguments[0].scrollTop+=10000;', scrollableElement)
    time.sleep(2)
    
    new_height = driver.execute_script('return document.body.scrollHeight')
    print(str(new_height) + " - " + str(last_height))
    if(new_height==last_height):
        break
    else:
        last_height = new_height
    

