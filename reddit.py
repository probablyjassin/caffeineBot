import os

import asyncpraw as praw
from dotenv import load_dotenv

#from discord.utils import get
load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv('CLIENT_ID'),
    client_secret = os.getenv('CLIENT_SECRET'),
    username = os.getenv('RDTUSER'),
    password = os.getenv('RDTPASSWORD'),
    user_agent = os.getenv('USER_AGENT')
)