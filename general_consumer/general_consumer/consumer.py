import asyncio
import nats
from nats.errors import TimeoutError
from common.protobuf.transformers import parse_post_from_string
from common.urls import NATS_URL
from common.stream_subjects import STREAM, MAIN_NEWS_SUBJECT, GENERAL_NEWS_STREAM, SPORTS_NEWS_STREAM
from common.configuration import NATS_TIMEOUT_IN_SECONDS

SPORT_KEYWORDS = ['sport']


async def main():
    nc = await nats.connect(servers=NATS_URL)
    js = nc.jetstream()

    await js.add_stream(name=STREAM, subjects=[MAIN_NEWS_SUBJECT])
    pub_sub = await js.pull_subscribe(MAIN_NEWS_SUBJECT, "psub")

    while True:
        try:
            msgs = await pub_sub.fetch(1, timeout=NATS_TIMEOUT_IN_SECONDS)
            for msg in msgs:
                await msg.ack()
                post = parse_post_from_string(msg.data)
                if any(keyword in post.title for keyword in SPORT_KEYWORDS):
                    await nc.publish(SPORTS_NEWS_STREAM, msg.data)
                else:
                    await nc.publish(GENERAL_NEWS_STREAM, msg.data)
        except TimeoutError:
            pass


if __name__ == '__main__':
    asyncio.run(main())
