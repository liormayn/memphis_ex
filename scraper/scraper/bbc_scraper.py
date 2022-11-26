import requests
from lxml import html

BASE_LINK = "http://www.bbc.com"


def extract_post_details(element):
    summary_xpath = './/p[contains(@class, "media__summary")]'
    title_xpath = './/a[@class="media__link"]'
    link_xpath = './/a[@class="media__link"]/@href'

    content = next(iter(element.xpath(summary_xpath)), None)
    title = next(iter(element.xpath(title_xpath)), None)
    link = next(iter(element.xpath(link_xpath)), '')
    return {
        'title': title.text.strip() if title is not None else '',
        'summary': content.text.strip() if content is not None else '',
        'link': f'{BASE_LINK}{link}'}


def get_news_posts():
    tree = html.fromstring(requests.get(BASE_LINK).content)
    media_item_xpath = '//*[contains(@class, "media-list__item media-list__item")]'
    data = tree.xpath(media_item_xpath)

    posts = []
    for element in data:
        post = extract_post_details(element)
        post_valid = post['title'] and post['link']
        if post_valid:
            posts.append(post)

    return posts
