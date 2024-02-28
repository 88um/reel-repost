
from database.access import root
from instagrapi.types import Media
from typing import List

def is_consumed(username: str, media : List[Media]):
        logs = root.get_target_logs(username)
        for post in media:
            if post.id not in logs:
                return False
        return True


def filter_posts(username, media : List[Media]):
    posts = []
    
    logs = root.get_target_logs(username)
    for post in media:
            if post.id not in logs :
                posts.append(post)
    return posts