import asyncio
import nats

from nats.errors import TimeoutError
from common.protobuf.transformers import parse_post_from_string
from common.urls import NATS_URL
from common.stream_subjects import MAIN_NEWS_SUBJECT


async def main():
    nc = await nats.connect(servers=NATS_URL)
    sub = await nc.subscribe(f"{MAIN_NEWS_SUBJECT}.*")

    try:
        while True:
            try:
                msg = await sub.next_msg(timeout=60)
                post = parse_post_from_string(msg.data)
                print({'subject': msg.subject,
                       'data': {'title': post.title, 'summary': post.summary, 'link': post.link}})
            except TimeoutError:
                pass
    finally:
        await sub.unsubscribe()
        await nc.drain()


if __name__ == '__main__':
    asyncio.run(main())
