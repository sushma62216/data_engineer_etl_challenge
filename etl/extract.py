import requests
import logging

def fetch_users():
    response= requests.get("https://jsonplaceholder.typicode.com/users")
    response.raise_for_status
    return response.json()

def fetch_posts():
    response= requests.get("https://jsonplaceholder.typicode.com/posts")
    response.raise_for_status
    return response.json()