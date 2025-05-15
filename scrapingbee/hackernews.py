import requests
from bs4 import BeautifulSoup

#r = requests.get('https://news.ycombinator.com')
#print(r.status_code)


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