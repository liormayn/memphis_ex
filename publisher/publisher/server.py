from flask import Flask
import json
from flask import request
from publisher.publish_handler import publish_posts
import logging
application = Flask(__name__)


@application.route('/posts', methods=['POST'])
async def post_posts():
    try:
        posts = json.loads(request.json)
        await publish_posts(posts)
        return 'success', 202
    except Exception as e:
        logging.exception(e)
        return e, 500


@application.route('/available', methods=['GET'])
async def available():
    return "i am alive", 202


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000)

