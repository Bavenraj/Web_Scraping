from bs4 import BeautifulSoup
from data_transform import mydict
import csv
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

csv_file = 'data/kfc_data_3_1.csv'
html_page_sources = []
logging.basicConfig(#filename="kfcscrapper.log", encoding="utf-8", filemode="a",
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_source(state_list = mydict):
    state_to_extract = state_list
    filtered_dict = {}
    for state, areas in mydict.items():
        if state in state_to_extract:
            filtered_dict[state] = areas
    #print(filtered_dict)
    for state, areas in filtered_dict.items():
        for area in areas:
            extract_data(state, area)
            #query = f"pageSource_3\KFC near {area}, {state}.html"
           # html_page_sources.append(query)
    #return html_page_sources
def get_final_url(map_url):
    options = Options()
    options.add_argument('--headless')  # optional
    driver = webdriver.Chrome(options=options)
    driver.get(map_url)
    time.sleep(1)
    final_url = driver.current_url
    driver.quit()
    return final_url

store_data = []
def extract_data(state, area):
    query = f"KFC near {area}, {state}"
    page_source = f"pageSource_3\KFC near {area}, {state}.html"
    logging.info(f'Extracting data from {page_source}')
    file = open(page_source)
    soup = BeautifulSoup(open(page_source, encoding='utf-8').read(), 'html.parser')
    if soup.find(name='div',attrs={"aria-label": f"Results for {query}"}):
        store_list = soup.find_all(name='div', attrs={"class": "Nv2PK"})
        for store in store_list:
            map_url = store.find(name='a', attrs={"class": "hfpxzc"})['href']
            #store_id = jslog.split("metadata:")[-1]
            name = store.find(name= 'div', attrs={"class": "qBF1Pd"})
            if store.find(string='Open') or store.find(string='Closed') or store.find(string='Open 24 hours'):
                store_status = 'Operating'
            elif store.find(string='Permanently closed'): 
                store_status = 'Permanently Closed'
            elif store.find(string='Temporarily closed'):
                store_status = 'Temporarily Closed'
            else:
                store_status = 'No status'

            review_available = store.find(name= 'span', attrs={"class": "fontBodyMedium"})
            if review_available is not None:
                if review_available.text == "No reviews":
                    ratings = 0
                    review = 0
                else:
                    ratings = store.find(name= 'span', attrs={"class": "MW4etd"}).text
                    review = store.find(name= 'span', attrs={"class": "UY7F9"}).text
        
                store_data.append({
                    'State': state,
                    'Area' : area,
                    'Map URL': map_url,
                    'Store Name' : name.text,
                    'Rating' : ratings,
                    'Review Count': review,
                    'Store Status': store_status                        
                })
            else: 
                pass  
    else: 
        name = soup.find(name= "h1")
        map_url = f"https://www.google.com/maps/search/KFC+near+{area},+{state}"
        #store_id = jslog.split("metadata:")[-1]
        if soup.find(string='Open') or soup.find(string='Closed') or soup.find(string='Open 24 hours'):
            store_status = 'Operating'
        elif soup.find(string='Permanently closed'):
            store_status = 'Permanently Closed'
        elif soup.find(string='Temporarily closed'):
            store_status = 'Temporarily Closed'
        else:
            store_status = 'No status'
            
        if soup.find(name= 'div', attrs={"class": "dmRWX", "style": "display: none"}):
            ratings = 0
            review = 0
        else:
            ratings = soup.find(name= 'div', attrs={"class": "F7nice"}).find_next().text
            review = soup.find(name= 'div', attrs={"class": "F7nice"})._last_descendant().text
            
        store_data.append({
            'State': state,
            'Area' : area,
            'Map URL': map_url,
            'Store Name' : name.text,
            'Rating' : ratings,
            'Review Count': review,
            'Store Status': store_status 
        })

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['State', 'Area', 'Map URL', 'Store Name','Rating', 'Review Count', 'Store Status'])
        writer.writeheader()
        for row in store_data:
            writer.writerow(row)
    #print(store_data) 

#print(extract_source(["W.P. Labuan", "W.P. Putrajaya"]))
extract_source()

#print(html_page_sources[221])