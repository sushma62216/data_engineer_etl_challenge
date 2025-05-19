from etl.extract import fetch_users, fetch_posts
from etl.load import load_users, load_posts, load_to_sqlserver
from etl.transform import join_users_posts

users = fetch_users()
posts = fetch_posts()

load_users(users)
load_posts(posts)

records = join_users_posts()
load_to_sqlserver(records)
