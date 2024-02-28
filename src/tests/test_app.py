import os
from reel_poster import ReelReposter
from dotenv import load_dotenv
load_dotenv()
session = os.getenv('TEST_SESSION')
client = ReelReposter()


#(reelposter) src % > python3 -m pytest tests/

def test_login():
    assert client.login(session)

def test_collect_and_save():
    posts = client.scrape_new_posts()
    assert posts 
    assert client.save_posts_to_folder(posts)


def test_post():
    post = client.fetch_saved_post()
    result = client.upload_saved_post(post)
    assert result 
