from bs4 import BeautifulSoup
from data_transform import mydict
import csv
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

csv_file = 'data/kfc_data_final_extraction.csv'
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


store_data = []
def extract_data(state, area):
    query = f"KFC near {area}, {state}"
    page_source = f"pageSource_detail\KFC near {area}, {state}.html"
    logging.info(f'Extracting data from {page_source}')
    file = open(page_source)
    soup = BeautifulSoup(open(page_source, encoding='utf-8').read(), 'html.parser')
    if soup.find(name='div',attrs={"class": "store_details"}):
        store_list = soup.find_all(name='div', attrs={"class": "store_details"})
        for store in store_list:
            name = store.find(name='h1', attrs={"class":"lfPIob"})
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
                    'Store Name' : name.text,
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

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['State', 'Area', 'Address', 'Store Name','Rating', 'Review Count', 'Store Status'])
        writer.writeheader()
        for row in store_data:
            writer.writerow(row)
    #print(store_data) 

#print(extract_source(["W.P. Labuan", "W.P. Putrajaya"]))
extract_source([ "W.P. Labuan", "W.P. Putrajaya", "Perlis", "Kelantan"])

#print(html_page_sources[221])