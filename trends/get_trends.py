#trending topics from google news
import os
from bs4 import BeautifulSoup
import requests
import time
from random import randint
import tweepy
import database_connection as db

def get_google_topics(url):
    trending_topics = []
    time.sleep(randint(0, 2))  # relax and don't let google be angry
    r = requests.get(url)
    content = r.text
    soup = BeautifulSoup(content, "html.parser")
    li_divs = soup.findAll("div", {"class": "topic"})
    for li_div in li_divs:
        trending_topics.append(li_div.a.text.lower())
    return trending_topics

def scrape_google_news():
    urls = ['https://news.google.com/',
            'https://news.google.com/news/section?cf=all&pz=1&topic=w',
            'https://news.google.com/news/section?cf=all&pz=1&topic=n']
    google_trends = []
    for url in urls:
        google_trends.extend(get_google_topics(url))
    return google_trends

def get_twitter_trends():
    CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
    CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
    US_WHOID = 23424977
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api = tweepy.API(auth)

    twitter_trends = api.trends_place(US_WHOID)
    return [t['name'] for t in twitter_trends[0]['trends'] if not t['name'].startswith('#')]

def get_new_trends():
    return set(scrape_google_news()+get_twitter_trends())

def update_trends_list():
    new_trends = [t.lower() for t in get_new_trends()][::-1]
    for t in new_trends:
       db.insert_trend(t)
