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

print("File Loaded into excel")

import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

host = "127.0.0.1"
port = "5432"
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB")

con = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
cur = con.cursor()

for link in links:
    cur.execute(""" INSERT into hn_links (id, title, url, rank)
        VALUES (%s, %s, %s, %s)
        """,
        (
            link['id'],
            link.find_all('td')[2].a.text,
            link.find_all('td')[2].a['href'],
            int(link.find_all('td')[0].span.text.replace('.', ''))
        )
    )
    
con.commit()
cur.close()
con.close()

print("File Loaded into database")

        