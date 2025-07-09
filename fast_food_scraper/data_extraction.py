from bs4 import BeautifulSoup
from data_transform import mydict
import csv
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from file import get_file, write_file


logging.basicConfig(filename="log/datascrapper.log", encoding="utf-8", filemode="a",
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_source(state_list = mydict):
    csv_file = get_file(file_name, fieldnames, state_list)
    state_to_extract = state_list
    filtered_dict = {}
    for state, areas in mydict.items():
        if state in state_to_extract:
            filtered_dict[state] = areas
    for state, areas in filtered_dict.items():
        for area in areas:
            store_data = extract_data(state, area)
            write_file(csv_file, fieldnames, store_data)

def extract_data(state, area):
    query = f"KFC near {area}, {state}"
    page_source = f"pageSource_detail\KFC near {area}, {state}.html"
    logging.info(f'Extracting data from {page_source}')
    file = open(page_source)
    soup = BeautifulSoup(open(page_source, encoding='utf-8').read(), 'html.parser')
    if soup.find(name='div',attrs={"class": "store_details"}):
        store_list = soup.find_all(name='div', attrs={"class": "store_details"})
        for store in store_list:
            name = store.find(name='h1', attrs={"class":"lfPIob"}).text
            address = store.find(name= 'button', attrs={"data-item-id": "address"})['aria-label']
            status = store.find(name="span", attrs={"class": "ZDu9vd"}).find_next().find_next().text
            if status in ['Open', 'Closed', 'Open 24 hours']:
                store_status = 'Operating'
            elif status == 'Permanently closed': 
                store_status = 'Permanently Closed'
            elif status =='Temporarily closed':
                store_status = 'Temporarily Closed'
            else:
                store_status = 'No status'

            if store.find(name= 'div', attrs={"class": "dmRWX", "style": "display: none"}):
                ratings = 0
                review = 0
            else:
                ratings = store.find(name= 'div', attrs={"class": "F7nice"}).find_next().text
                review = store.find(name= 'div', attrs={"class": "F7nice"})._last_descendant().text
        
                store_data.append({
                    'State': state,
                    'Area' : area,
                    'Address': address,
                    'Store Name' : name,
                    'Rating' : ratings,
                    'Review Count': review,
                    'Store Status': store_status                        
                })
    else: 
        name = soup.find(name= "h1")
        address = soup.find(name= 'button', attrs={"data-item-id": "address"})['aria-label']
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
            'Address': address,
            'Store Name' : name.text,
            'Rating' : ratings,
            'Review Count': review,
            'Store Status': store_status 
        })
    return store_data

file_name = 'data/kfc_data_final_extraction.csv'
fieldnames=['State', 'Area', 'Address', 'Store Name','Rating', 'Review Count', 'Store Status']
html_page_sources = []
store_data = []
#print(extract_source(["W.P. Labuan", "W.P. Putrajaya"]))
extract_source(["W.P. Labuan"])

