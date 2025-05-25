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

logging.info("Parsing page source with BeautifulSoup")
soup = BeautifulSoup(driver.page_source, 'html.parser')

logging.info("Finding all story titles on the page")
titles = soup.find_all('span', class_='titleline')

if titles:
    logging.info(f"Found {len(titles)} titles. Printing titles:")
    # Print each title
    for title in titles:
        title_link = title.find('a')
        if title_link:
            print(title_link.text)
else:
    logging.warning("No titles found on the page.")
    
#driver.save_screenshot('hn_homepage.png')
logging.info("Closing WebDriver")
driver.quit()