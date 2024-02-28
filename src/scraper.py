import time
from database.access import root
from instagrapi.types import Media
from typing import List
from datetime import datetime, timezone

class ScraperMixin:

    def is_consumed(self, username: str, media: List[Media]):
        # Check if every post on a targets page has already been posted by a username
        logs = root.get_target_logs(username)

    def _scrape_posts_from_account(self, target: str, amount: int = 10, min_likes: int = 0, min_comments: int = 0, age: int = 1, logs: List[str] = [], allowed_media_types: List[int] = [1, 2, 8]) -> List[Media]:
        posts = []
        user_id = self.__username_to_user_id(target)
        max_id = True
        while max_id:
            if max_id is True:
                max_id = ""
            if len(posts) >= amount:
                posts = posts[:amount]
                break
            posts_chunk, max_id = self.client.user_medias_paginated_v1(
                user_id, amount, max_id)
            for post in posts_chunk:
                if (
                    post.like_count >= min_likes
                    and post.comment_count >= min_comments
                    and post.taken_at
                    and (
                        datetime.now(timezone.utc) -
                        post.taken_at.replace(tzinfo=timezone.utc)
                    ).total_seconds() / 3600 <= age
                    and str(post.pk) not in logs
                    and post.media_type in allowed_media_types
                ):
                    posts.append(post)
            time.sleep(2)

        return posts

    def __username_to_user_id(self, username: str) -> str:
        target = root.get_target(username)
        if not target:
            user_id = self.client.user_id_from_username(username)
            root.add_target(username, user_id)
            return user_id
        return target.user_id
