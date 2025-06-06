from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


import logging

# Set up logging to troubleshoot if anything goes wrong
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Initializing WebDriver")
options = Options()
#options = get_default_chrome_options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)

logging.info("Loading Selenium Documentations")
driver.get("https://www.selenium.dev/selenium/web/web-form.html")
#driver.implicitly_wait(1)

#title = driver.title
#print(title)

logging.info("Locating input text box and button")
text_box = driver.find_element(by = By.NAME, value="my-text")
submit_button = driver.find_element(by = By.CSS_SELECTOR, value="button")

logging.info("Submiting form with text box filled")
text_box.send_keys("Selenium")
submit_button.click()

logging.info("Locating and printing success message")
message = driver.find_element(by=By.ID, value="message")
text = message.text
print(text)

logging.info("Closing WebDriver")
driver.quit()