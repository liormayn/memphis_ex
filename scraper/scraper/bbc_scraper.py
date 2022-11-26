import requests
from lxml import html

BASE_LINK = "http://www.bbc.com"


def get_news_posts():
    tree = html.fromstring(requests.get(BASE_LINK).content)
    media_item_xpath = '//*[contains(@class, "media-list__item media-list__item")]'
    data = tree.xpath(media_item_xpath)

    posts = []
    for element in data:
        content = next(iter(element.xpath('.//p[contains(@class, "media__summary")]')), None)
        title = next(iter(element.xpath('.//a[@class="media__link"]')), None)
        link = next(iter(element.xpath('.//a[@class="media__link"]/@href')), '')

        if (title and title.text) or link:
            posts.append({
                'title': title.text.strip() if title is not None else '',
                'summary': content.text.strip() if content is not None else '',
                'link': f'{BASE_LINK}{link}'})

    return posts
