import requests
from bs4 import BeautifulSoup

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

r = requests.get('https://news.ycombinator.com')
#print(r.status_code)
soup = BeautifulSoup(r.text, 'html.parser')
links = soup.findAll('tr', class_='athing')

data = []

for link in links:
    data_link = {
        'id': link['id'],
        'title': link.find_all('td')[2].a.text,
        "url": link.find_all('td')[2].a['href'],
        "rank": int(link.find_all('td')[0].span.text.replace('.', ''))
    }
    data.append(data_link)

#print(formatted_links)

import csv


csv_file = 'hacker_news_posts.csv'

with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['id', 'title', 'url', 'rank'])
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("File Loaded")
        