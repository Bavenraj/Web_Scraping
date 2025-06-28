from bs4 import BeautifulSoup
from data_transform import mydict
html_page_sources = []
def extract_source(state_list = mydict):
    
    state_to_extract = state_list
    filtered_dict = {}
    for state, areas in mydict.items():
        if state in state_to_extract:
            filtered_dict[state] = areas
    #print(filtered_dict)
            
    for state, areas in filtered_dict.items():
        for area in areas:
            query = f"KFC near {area}, {state}"
            html_page_sources.append(query)
    return html_page_sources

def extract_data(page_sources):
    for page_source in page_sources:
        soup = BeautifulSoup(page_source, 'html.parser')
        soup.find_all
extract_source()
print(html_page_sources[221])