from bs4 import BeautifulSoup
from data_transform import mydict
import csv
import logging

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

store_data = []
def extract_data(state, area):
    
    page_source = f"pageSource_3\KFC near {area}, {state}.html"
    logging.info(f'Extracting data from {page_source}')
    file = open(page_source)
    soup = BeautifulSoup(open(page_source, encoding='utf-8').read(), 'html.parser')
    if soup.find(name = 'a', attrs={"class": "hfpxzc"}):      
        classes = soup.find_all(name='div', attrs={"class": "fontBodyMedium"})
        for store in classes:
            name = store.find(name= 'div', attrs={"class": "fontHeadlineSmall"})
            if name is not None:
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
                        'Store Name' : name.text,
                        'Rating' : ratings,
                        'Review Count': review
                    })
                else: 
                    pass
        
    else: 
        name = soup.find(name= "h1")
        if name is not None:
            if soup.find(name= 'div', attrs={"class": "dmRWX", "style": "display: none"}):
                ratings = 0
                review = 0
            else:
                ratings = soup.find(name= 'div', attrs={"class": "F7nice"}).find_next().text
                review = soup.find(name= 'div', attrs={"class": "F7nice"})._last_descendant().text
                
            store_data.append({
                'State': state,
                'Area' : area,
                'Store Name' : name.text,
                'Rating' : ratings,
                'Review Count': review
            })

    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['State', 'Area', 'Store Name','Rating', 'Review Count'])
        writer.writeheader()
        for row in store_data:
            writer.writerow(row)
    #print(store_data) 

#print(extract_source(["W.P. Labuan", "W.P. Putrajaya"]))
extract_source()#["W.P. Kuala Lumpur"]))

#print(html_page_sources[221])