import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)
    
async def scrape():
    urls = [f'https://news.ycombinator.com/news?p={i}' for i in range (1, 26)]
    #print(urls)
    html_pages = await fetch_all(urls)
    all_links = []
    for html in html_pages:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.findAll('tr', class_='athing')
        for link in links:
            data = {
                'id': link['id'],
                'title': link.find_all('td')[2].a.text,
                'url': link.find_all('td')[2].a['href'],
                'rank': int(link.find_all('td')[0].span.text.replace('.', ''))
            }
            all_links.append(data)
            
    #print("File Loaded into excel")
    csv_file = 'hacker_news_posts_async.csv'

    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'title', 'url', 'rank'])
        writer.writeheader()
        for row in all_links:
            writer.writerow(row)
    #for link in all_links:
        #print(f"ID: {link['id']}, Title: {link['title']}, URL: {link['url']}, Rank: {link['rank']}")
    
    #return all_links
    
        
asyncio.run(scrape())

#urls = ['https://news.ycombinator.com/news?p=1'] * 25
#print(urls)