import json
import time
import random
import os
from scraper import ScraperMixin
from utils import *
from datetime import datetime, timezone
from typing import List, Dict, Optional
from instagrapi.types import Media
from instagrapi import Client
from exceptions import *
from database.access import root
from database.models import *


class ReelReposter(ScraperMixin):

    def __init__(self, config_file: str = "config.json", media_folder: str = "media"):
        with open(config_file, 'r') as f:
            self.config = json.loads(f.read())

        self.done = 0
        self.error = 0
        self.media_folder = media_folder
        self.init()

    def init(self):
        self.targets: List[str] = self.config['targets']
        self.captions = self.config['captions']
        self.amount = self.config['amount_to_scrape']
        self.min_likes = self.config['minimum_likes']
        self.min_comments = self.config['minimum_comments']
        self.sleep_time = self.config['posting_interval_seconds']
        self.age = self.config['age_limit_hours']
        self.allowed_media_types = self.config['allowed_media_types']
        self.extra_data = self.config['extra_data']
        self.check_viral_posts = self.config['check_viral_posts']
        self.viral_likes = self.config['viral_likes']
        self.pinned_comments = self.config['pinned_comments']
        self.client = Client(proxy=self.config['proxy'])

    def login(self, username: str, password: str = "") -> bool:

        # Login by sessionid
        if '%' in username:
            self.client.login_by_sessionid(username)
            account_info = self.client.account_info()
            self.client.username = account_info.username

        # Login by user/pass
        else:
            old_acc = root.get_account(username)
            if not old_acc:
                print("Logging in...")
                self.client.login(username, password)
                root.add_account(username, password,
                                 self.client.get_settings())
            else:
                self.client.set_settings(json.loads(old_acc.credentials))
                self.client.username = old_acc.username
                self.client.password = old_acc.password

        print("Logged In!")

        time.sleep(1)
        return True

    
    def scrape_new_posts(self) -> List[Media]:
       # self.init() You can uncomment this to refresh the config
        posts = []

        # Posts we have already seen and posted will be skipped
        logs = root.get_target_logs(self.client.username)
        current_saved = [i.pk for i in root.get_all_media()]
        logs.extend(current_saved)
        # Loop through the targets until one of them has fresh posts
        for target in self.targets:
            if len(posts) >= self.amount:
                posts = posts[:self.amount]
                break
            gathered_posts = self.__scrape_posts_from_account(
                target, self.amount, self.min_likes, self.min_comments, self.age, logs, self.allowed_media_types)
            for post in gathered_posts:
                posts.append(post)

            print(
                f"[{self.client.username}] Collected {len(gathered_posts)}x new posts from {target}")

        # No posts were found lel
        if not posts:
            raise TargetsConsumed(
                f"Error [{self.client.username}]: Unable to find posts. Please update filters or change targets to continue.")

        return posts

    
    def save_posts_to_folder(self, posts: List[Media]) -> bool:
        for post in posts:
            video_path = None
            thumbnail_path = None
            paths = []
            filename = f"{post.user.username}_{post.pk}"
            if post.media_type == 2:
                video_path = self.client.clip_download_by_url(
                    post.video_url, filename+"mp4", self.media_folder)
                thumbnail_path = self.client.photo_download_by_url(
                    post.thumbnail_url, filename+"jpg", self.media_folder)
            elif post.media_type == 1:
                thumbnail_path = self.client.photo_download_by_url(
                    post.thumbnail_url, filename+"jpg", self.media_folder)
            else:
                paths = self.client.album_download(post.id, self.media_folder)
                paths = [str(path) for path in paths]

            # Because the paths field is unqiue in DB
            paths = paths if paths else [f'{time.time()}']
            new_saved_post = SavedMedia(
                pk=str(post.pk),
                media_type=post.media_type,
                like_count=post.like_count,
                comment_count=post.comment_count,
                caption=post.caption_text,
                owner=post.user.username,
                paths=json.dumps(paths),
                video_path=str(video_path),  
                thumbnail_path=str(thumbnail_path),
            )
            root.add_saved_media(new_saved_post)
        
        return True

    
    def fetch_saved_post(self) -> Optional[SavedMedia]:
        saved_posts = root.get_all_media()
        if not saved_posts:
            raise NoMorePosts("Please fetch and save new posts.")

        random_post = random.choice(saved_posts)
        random_post.paths = json.loads(random_post.paths)
        return random_post


    def upload_saved_post(self, post: SavedMedia) -> Media:
        caption = random.choice(self.captions)
        response = None
        if post.media_type == 8:
            response = self.client.album_upload((
                post.paths), caption, extra_data=self.extra_data)
        elif post.media_type == 2:
            response = self.client.clip_upload(
                (post.video_path), caption, post.thumbnail_path,  extra_data=self.extra_data)
        else:
            response = self.client.photo_upload(
                (post.thumbnail_path), caption,   extra_data=self.extra_data)

        self.clean_up_post(post)
        return response

    
    def clean_up_post(self, post : SavedMedia):
        root.add_target_log(self.client.username, str(post.pk))
        root.delete_saved_media(post.id)
        media_files_to_remove = [
                os.path.join(self.media_folder, filename)
                for filename in os.listdir(self.media_folder)
                if str(post.pk) in filename
            ]

        for media_file_to_remove in media_files_to_remove:
                os.remove(media_file_to_remove)

    def has_more_posts(self):
        return len(root.get_all_media()) > 0
    
    def check_viral(self):
        if not self.check_viral_posts:
            return 

        viral_posts = self.__scrape_posts_from_account(
            self.client.username,
            amount=10,
            min_likes=self.viral_likes ,
            age = 9999
        )

        for post in viral_posts:
            comment = self.client.media_comment(post.id, random.choice(self.pinned_comments))
            self.client.comment_pin(post.id, comment.pk)
            print("Successfully commented and pinned on viral post!")


    def sleep(self):
        time.sleep(self.sleep_time)
    

   

    
    
   
