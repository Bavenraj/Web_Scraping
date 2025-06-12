from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Initializing WebDriver")

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
driver.set_window_size(1300,800)

logging.info("Loading Google Maps")
driver.get("https://www.google.com/maps/")
time.sleep(5)

logging.info("Getting input search box")
input = driver.find_element(by = By.CLASS_NAME, value = "searchboxinput")
input.clear()

logging.info("Searching for location")
input.send_keys("kfc selangor", Keys.ENTER)
time.sleep(5)


