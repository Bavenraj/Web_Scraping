from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Initializing WebDriver")

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
driver.maximize_window()

def generate_grid_boxes(min_lat, max_lat, min_lon, max_lon, step_km=5):
    from geopy.distance import distance
    import geopy

    # Approximate steps in degrees for latitude and longitude
    def step_in_degrees(lat, km):
        # 1 deg latitude ≈ 111 km
        lat_step = km / 111
        # 1 deg longitude ≈ varies by latitude
        lon_step = km / (111 * abs(math.cos(math.radians(lat))) + 1e-6)
        return lat_step, lon_step

    import math
    boxes = []
    lat = min_lat
    while lat < max_lat:
        lat_step, _ = step_in_degrees(lat, step_km)
        lon = min_lon
        while lon < max_lon:
            _, lon_step = step_in_degrees(lat, step_km)
            boxes.append({
                "center_lat": lat + lat_step / 2,
                "center_lon": lon + lon_step / 2,
                "lat_range": (lat, lat + lat_step),
                "lon_range": (lon, lon + lon_step)
            })
            lon += lon_step
        lat += lat_step
    return boxes


def load_map():
    logging.info("Loading Google Maps")
    driver.get("https://www.google.com/maps/")
    time.sleep(5)

def find_location(query):
    logging.info("Getting input search box")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'searchboxinput')))
    input = driver.find_element(by = By.CLASS_NAME, value = "searchboxinput")
    input.clear()
    
    logging.info(f"Searching for {query}:")
    input.send_keys(query, Keys.ENTER)
    time.sleep(5)
    
    logging.info("Looking for scrollable element")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[aria-label='Results for {query}']")))
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
states_and_federal_territorie = [ "Selangor", "Labuan"]
count = []
data = []
for state_fd in states_and_federal_territorie:
    load_map()
    query = f"KFC {state_fd}"
    count.append(find_location(query = query))
    data_link = {
        'Location': query,
        'Count': count[-1]
    }
    data.append(data_link)
    
print(data)

import csv
csv_file = 'kfc_data.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['Location', 'Count'])
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("File Loaded into csv")


