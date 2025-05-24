from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
executable_path=r"C:\Program Files (x86)\chromedriver\chromedriver.exe"

driver = webdriver.Chrome(service=Service(executable_path))
driver.get("https://news.ycombinator.com/")
driver.save_screenshot('hn_homepage.png')
driver.quit()