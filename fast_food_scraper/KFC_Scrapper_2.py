from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data_transform import mydict
import csv
csv_file = 'data/kfc_data_3.csv'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Initializing WebDriver")
options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
driver.maximize_window()

def load_map():
    logging.info("Loading Google Maps")
    driver.get("https://www.google.com/maps/@4.619127,108.9124153,6z?entry=ttu&g_ep=EgoyMDI1MDYxNy4wIKXMDSoASAFQAw%3D%3D")
    time.sleep(3)

def find_state(query):
    logging.info("Getting input search box")
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'searchboxinput')))
    input = driver.find_element(by = By.CLASS_NAME, value = "searchboxinput")
    input.clear()
    
    logging.info(f"Searching for {query}:")
    input.send_keys(query, Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(3) 
    
    logging.info("Looking for nearby location button")
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[aria-label='Nearby']")))
    NearbyButton = driver.find_element(by=By.CSS_SELECTOR, value =f"[aria-label='Nearby']")
    NearbyButton.click()
    time.sleep(1)
    
    return driver

def find_nearby_location(driver, query):    

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "searchboxinput")))
    input = driver.find_element(by=By.ID, value = "searchboxinput")
    input.clear()
    
    logging.info(f"Searching for {query}:")
    input.send_keys(query, Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(3)
    
    try: 
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[aria-label='Results for {query}']")))
        scrollableElement = driver.find_element(by=By.CSS_SELECTOR, value =f"[aria-label='Results for {query}']")
        initial_count = 0
        while True:
            logging.info("Found. Scrolling search results")
            for _ in range(3):
                driver.execute_script('arguments[0].scrollBy(0,1000);', scrollableElement)
                time.sleep(1)
            
            final_count = len(driver.find_elements(by=By.CLASS_NAME, value = "hfpxzc"))
            #print(str(initial_count)+" - "+ str(final_count))
            time.sleep(2)
            
            if(initial_count!=final_count):
                initial_count = final_count
            else:
                pageSource = driver.page_source
                with open(f"pageSource_1/{query}.html", "w", encoding="utf-8") as file:
                    file.write(pageSource)
                return final_count
    except:
        time.sleep(2)
        pageSource = driver.page_source
        with open(f"pageSource_1/{query}.html", "w", encoding="utf-8") as file:
            file.write(pageSource)
        final_count = 1
        return final_count
    
           
count = []
data = []
def start_scrape(state_list = mydict):
    
    state_to_scrape = state_list
    filtered_dict = {}
    for state, areas in mydict.items():
        if state in state_to_scrape:
            filtered_dict[state] = areas
    #print(filtered_dict)
            
    for state, areas in filtered_dict.items():
        load_map()
        driverr = find_state(state)
        for area in areas:
            query = f"KFC near {area}, {state}"
            count.append(find_nearby_location(driver=driverr, query = query))
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

start_scrape("W.P. Labuan")


