from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import pandas as pd
csv_file = 'data/kfc_new_data.csv'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Initializing WebDriver")

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
driver.maximize_window()

def load_map():
    logging.info("Loading Google Maps")
    driver.get("https://www.google.com/maps/")
    time.sleep(3)

def find_location(query):
    logging.info("Getting input search box")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'searchboxinput')))
    input = driver.find_element(by = By.CLASS_NAME, value = "searchboxinput")
    input.clear()
    
    logging.info(f"Searching for {query}:")
    input.send_keys(query, Keys.ENTER)
    time.sleep(5)
    driver.refresh()
    time.sleep(5)
    logging.info("Looking for scrollable element")
    try: 
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[aria-label='Results for {query}']")))
        scrollableElement = driver.find_element(by=By.CSS_SELECTOR, value =f"[aria-label='Results for {query}']")
        initial_count = 0
        while True:
            logging.info("Scrolling search results")
            for _ in range(3):
                driver.execute_script('arguments[0].scrollBy(0,1000);', scrollableElement)
                time.sleep(1)
            
            logging.info("Calculation difference in search results count")
            final_count = len(driver.find_elements(by=By.CLASS_NAME, value = "hfpxzc"))
            #print(str(initial_count)+" - "+ str(final_count))
            time.sleep(2)
            pageSource = driver.page_source
            with open(f"pageSource/{query}.html", "w", encoding="utf-8") as file:
                file.write(pageSource)
            
            if(initial_count!=final_count):
                initial_count = final_count
            else:
                return final_count
    except:
        time.sleep(2)
        pageSource = driver.page_source
        with open(f"pageSource/{query}.html", "w", encoding="utf-8") as file:
            file.write(pageSource)
        final_count = 1
        return final_count
    
count = []
data = []
kfc = pd.read_csv('data/kfc_data.csv')
kfc = kfc[kfc['Count'] == 1]
mydict = {}
for state, area in kfc.groupby('State'):
    mydict.update({state: area["Area"].to_list()})

print(mydict)
def start_scrape(state_list = mydict):
                
    for state, areas in state_list.items():
        for area in areas:
            load_map()
            query = f"KFC near {area}, {state}"
            count.append(find_location(query = query))
            data_link = {
                'State': state,
                'Area' : area,
                'Count': count[-1]
            }
            data.append(data_link) 
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['State','Area', 'Count'])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
 
        print(f"Data for {query} was loaded into csv")
    print(data)

start_scrape()


