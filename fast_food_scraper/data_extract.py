from bs4 import BeautifulSoup
from data_transform import mydict
import csv
import logging

csv_file = 'data/kfc_data_4.csv'
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
            query = f"pageSource_3\KFC near {area}, {state}.html"
            html_page_sources.append(query)
    return html_page_sources

store_data = []
'''h1 -> store Name
jANrlb  -> store rating
HHrUdb or F7nice  -> store review'''
def extract_data(page_sources):
    for page_source in page_sources:
        logging.info(f'Extracting data from {page_source}')
        file = open(page_source)
        soup = BeautifulSoup(open(page_source, encoding='utf-8').read(), 'html.parser')
        if soup.find(name = 'a', attrs={"class": "hfpxzc"}):      
            classes = soup.find_all(name='div', attrs={"class": "fontBodyMedium"})
            for store in classes:
                name = store.find(name= 'div', attrs={"class": "fontHeadlineSmall"})
                review_available = store.find(name= 'span', attrs={"class": "fontBodyMedium"})
                if review_available is not None:
                    if review_available.text == "No reviews":
                        ratings = 0
                        review = 0
                    else:
                        ratings = store.find(name= 'span', attrs={"class": "MW4etd"})
                        review = store.find(name= 'span', attrs={"class": "UY7F9"})
                        if name is not None:
                            store_data.append({
                                'Store Name' : name.text,
                                'Rating' : ratings.text,
                                'Review Count': review.text
                            })
            
        else: 
            name = soup.find(name= "h1")
            #if soup.find(name= 'div', attrs={"class": "F7nice"}) is no
            ratings = soup.find(name= 'div', attrs={"class": "F7nice"})
            review = soup.find(name= 'div', attrs={"class": "F7nice"})
            #review._last_descendant().text
            if name is not None:
                store_data.append({
                    'Store Name' : name.text,
                    'Rating' : ratings.find_next().text,
                    'Review Count': review._last_descendant().text
                })

    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Store Name','Rating', 'Review Count'])
        writer.writeheader()
        for row in store_data:
            writer.writerow(row)
    #print(store_data) 

#print(extract_source(["W.P. Labuan", "W.P. Putrajaya"]))
extract_data(extract_source())#["W.P. Kuala Lumpur"]))

#print(html_page_sources[221])