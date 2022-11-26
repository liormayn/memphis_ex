import common.protobuf.post_pb2 as Post


def parse_post_from_string(string):
    proto_post = Post.Post()
    proto_post.ParseFromString(string)
    return proto_post


def parse_post_to_string(title, summary, link):
    proto_post = Post.Post()
    proto_post.title = title
    proto_post.summary = summary
    proto_post.link = link
    return proto_post.SerializeToString()