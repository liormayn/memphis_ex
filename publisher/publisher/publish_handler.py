import nats
from common.protobuf.transformers import parse_post_to_string
from common.urls import NATS_URL
from common.stream_subjects import MAIN_NEWS_SUBJECT, STREAM


async def publish_posts(posts):
    try:
        client = await nats.connect(NATS_URL)
        js = client.jetstream()
        await js.add_stream(name=STREAM, subjects=[MAIN_NEWS_SUBJECT])

        for post in posts:
            parsed_post = parse_post_to_string(title=post['title'], summary=post['summary'], link=post['link'])
            await js.publish("posts", parsed_post)

        await client.drain()

    except Exception as e:
        print(f'exception publishing posts:  {e}')