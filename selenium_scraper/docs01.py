from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome()

driver.get("https://www.selenium.dev/selenium/web/web-form.html")
#driver.implicitly_wait(1)

title = driver.title
text_box = driver.find_element(by = By.NAME, value="my-text")
submit_button = driver.find_element(by = By.CSS_SELECTOR, value="button")
text_box.send_keys("Selenium")
submit_button.click()
print(title)

#driver.quit()