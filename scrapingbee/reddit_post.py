import praw
import csv
import os
from dotenv import load_dotenv
load_dotenv()
import logging

# Set up logging to troubleshoot if anything goes wrong
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client_id = os.getenv("reddit_client_id")
client_secret = os.getenv("reddit_secret_key")

logging.info('Setting up Reddit API credentials')
reddit = praw.Reddit(client_id= client_id, client_secret=client_secret, user_agent='top-post')

logging.info('Getting the top 1,000 posts from the subreddit')
top_posts = reddit.subreddit('Entrepreneur').top(limit=10)


logging.info('Printing one output as for testing purpose')
for post in top_posts:
        print(f"{post.title} , {post.score} , {post.num_comments} , {post.author}")
        break
    
logging.info('Writting data into csv file')
with open('top_1000.csv', 'w', newline='') as file:
    fieldnames = ['title', 'score', 'num_comments', 'author']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for post in top_posts:
        writer.writerow({
            'title': post.title,
            'score': post.score,
            'num_comments': post.num_comments,
            'author': str(post.author)
        })