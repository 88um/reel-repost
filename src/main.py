import os
from reel_poster import ReelReposter
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    session_id = os.getenv('TEST_SESSION')
    client = ReelReposter(config_file='config.json', media_folder='media')
    loggedin = False

    if session_id:
        loggedin = client.login(session_id)
    
    
    else:
        username = input("[LOGIN] Type your username: ")
        password = input("[LOGIN] Type your password: ")
        loggedin = client.login(username, password)
    #Login either by session or credentials
    
    while loggedin:
        if not client.has_more_posts():
            # Collect posts and save them to folder
            posts = client.scrape_new_posts()
            client.save_posts_to_folder(posts)

        #Fetch a saved post from our database
        post = client.fetch_saved_post()

        #Now upload it!
        uploaded = client.upload_saved_post(post)
        print(f"[{client.client.username}] Successfully uploaded post! | Total Done: {client.done}") if uploaded else print("Failed to upload post!")

        #Now check if any of my recent posts are going viral, if so - comment and tell people to follow me
        client.check_viral()

        #Okay youre good for now, sleep a little
        client.sleep()
