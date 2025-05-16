import requests
from bs4 import BeautifulSoup

r = requests.get('https://news.ycombinator.com')
#print(r.status_code)
soup = BeautifulSoup(r.text, 'html.parser')
links = soup.findAll('tr', class_='athing')

formatted_links = []

for link in links:
    data = {
        'id': link['id'],
        'title': link.find_all('td')[2].a.text,
        "url": link.find_all('td')[2].a['href'],
        "rank": int(link.find_all('td')[0].span.text.replace('.', ''))
    }
    formatted_links.append(data)

print(formatted_links)

"""
BASE_URL = 'https://news.ycombinator.com'
USERNAME = "admin101"
PASSWORD = "admin101"

s = requests.Session()

data = { "acct": USERNAME, "pw": PASSWORD}
r = s.post(f'{BASE_URL}/login', data=data)

soup = BeautifulSoup(r.text, 'html.parser')
if soup.find(id='logout') is not None:
    print('Successfully logged in')
else:
    print('Authentication Error')
    
"""