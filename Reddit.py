import praw
import os
from dotenv import load_dotenv 
load_dotenv("client.env") 
reddit = praw.Reddit(
    client_id=os.getenv("Shubot_CLIENT_ID"),
    client_secret=os.getenv("Shubot_CLIENT_SECRET"),
    user_agent=os.getenv("Shubot_USER_AGENT"),
    username=os.getenv("Shubot_USERNAME"),
    password=os.getenv("Shubot_PASSWORD"))
