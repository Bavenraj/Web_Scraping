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
from selenium.common.exceptions import TimeoutException

csv_file = 'data/kfc_data_final.csv'

logging.basicConfig(filename="mapscrapper.log", encoding="utf-8", filemode="a",
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    logging.info("Getting nearby location input search box ")
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "searchboxinput")))
    input = driver.find_element(by=By.ID, value = "searchboxinput")
    input.clear()
    
    logging.info(f"Searching for {query}:")
    input.send_keys(query, Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(3)
    
    try:
        logging.info("Looking for Searched Results")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[aria-label='Results for {query}']")))
        scrollableElement = driver.find_element(by=By.CSS_SELECTOR, value =f"[aria-label='Results for {query}']")
        initial_count = 0
        logging.info("Found. Scrolling search results list")
        while True:
            for _ in range(3):
                driver.execute_script('arguments[0].scrollBy(0,1000);', scrollableElement)
                time.sleep(1)
                
            final_count = len(driver.find_elements(by=By.CLASS_NAME, value = "hfpxzc"))
            time.sleep(2)
            
            if(initial_count!=final_count):
                initial_count = final_count
            else:
                #title = driver.find_element(by=By.CLASS_NAME, value="fontTitleLarge")
                driver.execute_script("arguments[0].scrollTop=0;", scrollableElement)
                time.sleep(0.5)
                #driver.execute_script("arguments[0].scrollIntoView(false);", title)
                result_list = driver.find_elements(by=By.CLASS_NAME, value = "hfpxzc")
                for result in result_list:
                    driver.execute_script("arguments[0].scrollIntoView(true);", result)
                    result.click()
                    time.sleep(2)
                    page_html = driver.page_source
                    soup = BeautifulSoup(page_html, "html.parser")
                    store_name = soup.find(name="span", attrs={"jsname":"r4nke"}).text
                    store_details = soup.find(name= 'div', attrs={"class": "lMbq3e"})
                    details.append(str("<div class='store_details'>"))
                    details.append(str(store_details))
                    store_region = soup.find(name='div', attrs={"aria-label":f"Information for {store_name}"})
                    details.append(str(store_region))
                    details.append(str("</div>"))
                    
                logging.info("Extracting Page Source")
                with open(f"pageSource_detail/{query}.html", "w", encoding="utf-8") as file:
                    file.write("<html><head><meta charset='utf-8'></head><body>")
                    file.write("".join(details))
                    file.write("</body></html>")
                logging.info(f"{query}: {final_count}")
                return final_count
    except TimeoutException:
        logging.info("Result list not found. Only One Result available")
        time.sleep(2)
        logging.info("Extracting Page Source")
        pageSource = driver.page_source
        with open(f"pageSource_detail/{query}.html", "w", encoding="utf-8") as file:
            file.write(pageSource)
        final_count = 1
        logging.info(f"{query}: {final_count}")
        return final_count
           
count = []
data = []
details = []
def start_scrape(state_list = mydict):
    
    state_to_scrape = state_list
    filtered_dict = {}
    for state, areas in mydict.items():
        if state in state_to_scrape:
            filtered_dict[state] = areas
    #print(filtered_dict)
            
    for state, areas in filtered_dict.items():
        for area in areas:
            start_time = time.perf_counter()
            load_map()
            driverr = find_state(state)
            query = f"KFC near {area}, {state}"
            count.append(find_nearby_location(driver=driverr, query = query))
            end_time = time.perf_counter()
            scraping_duration = end_time - start_time

            data_link = {
                'State': state,
                'Area' : area,
                'Count': count[-1],
                'Duration': round(scraping_duration, 2)
            }
            data.append(data_link) 
            
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['State','Area', 'Count', 'Duration'])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
 
        logging.info(f"Data for {state} was loaded into csv")
    print(data)

start_scrape(["W.P. Labuan"]) #yasminwijnaldum 