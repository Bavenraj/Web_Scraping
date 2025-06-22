from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging
from bs4 import BeautifulSoup

# Set up logging to troubleshoot if anything goes wrong
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
executable_path=r"C:\Program Files (x86)\chromedriver\chromedriver.exe"

logging.info("Initializing WebDriver")
driver = webdriver.Chrome(service=Service(executable_path))

logging.info("Loading Hacker News homepage")
driver.get("https://news.ycombinator.com/")

logging.info("Locating the third 'td' of the first 'tr' which contains the article's title and link")
title_element = driver.find_element_by_xpath('//tr[@class="athing"]/td[3]/a')

logging.info("Extracting and printing the text from the located WebElement")
print(title_element.text)

logging.info("Clicking on the link to navigate to the article's page")
title_element.click()

logging.info("Printing the current URL after clicking")
print(driver.current_url)
    
logging.info("Closing WebDriver")
driver.quit()