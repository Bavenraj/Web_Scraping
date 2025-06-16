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

def load_map():
    logging.info("Loading Google Maps")
    driver.get("https://www.google.com/maps/")
    time.sleep(5)

def find_location(query):
    logging.info("Getting input search box")
    input = driver.find_element(by = By.CLASS_NAME, value = "searchboxinput")
    input.clear()
    
    logging.info(f"Searching for {query}:")
    input.send_keys(query, Keys.ENTER)
    time.sleep(5)
    
    logging.info("Looking for scrollable element")
    scrollableElement = driver.find_element(by=By.CSS_SELECTOR, value =f"[aria-label='Results for {query}']")
    initial_count = 0
    while True:
        logging.info("Scrolling search results")
        for _ in range(3):
            driver.execute_script('arguments[0].scrollBy(0,1000);', scrollableElement)
            time.sleep(1)
        
        logging.info("Calculation difference in search results count")
        final_count = len(driver.find_elements(by=By.CLASS_NAME, value = "hfpxzc"))
        print(str(initial_count)+" - "+ str(final_count))
        time.sleep(2)
        
        if(initial_count!=final_count):
            initial_count = final_count
        else:
            return final_count
            
states_and_federal_territories = ["Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang",
    "Penang", "Perak", "Perlis", "Sabah", "Sarawak", "Selangor", "Terengganu", 
    "Kuala Lumpur", "Putrajaya", "Labuan" # Federal Territory
]
count = []
data = []
for state_fd in states_and_federal_territories:
    load_map()
    query = "KFC " + state_fd
    count.append(find_location(query = query))
    data_link = {
        'Location': query,
        'Count': count[-1]
    }
    data.append(data_link)
    
print(data)


