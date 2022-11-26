import json
import asyncio
import requests
import logging

from scraper.bbc_scraper import get_news_posts as get_bbc_posts
from scraper.utils import every
from common.urls import API_URL
from common.configuration import SCRAPER_INTERVAL_IN_SECONDS

PUBLISHER_API = f'http://{API_URL}'
POST_ENDPOINT = 'posts'

news_retrievers = [get_bbc_posts]


def get_posts():
    try:
        posts = []
        for news_retriever in news_retrievers:
            posts.extend(news_retriever())
        return posts
    except:
        logging.exception("failed retrieving posts")
        raise


def send_posts(posts):
    try:
        url = f'{PUBLISHER_API}/{POST_ENDPOINT}'
        requests.post(url, json=json.dumps(posts))
        logging.info(requests.status_codes)
    except:
        logging.exception('failed sending posts')
        raise


def submit_new_posts():
    logging.info('starting new post process')
    posts = get_posts()
    send_posts(posts)


if __name__ == '__main__':
    a = asyncio.get_event_loop()
    a.create_task(every(SCRAPER_INTERVAL_IN_SECONDS, submit_new_posts))
    a.run_forever()
