from collections import defaultdict
from telegram import Update
import pickle

user_access = defaultdict(lambda: "user")

def load_user_access():
    global user_access
    try:
        with open("user_access.pkl", "rb") as f:
            user_access = defaultdict(lambda: "user", pickle.load(f))
        print("User access level loaded successfully.")
    except FileNotFoundError:
        print("No existing access file found. Starting fresh.")
        user_access = defaultdict(lambda: "user")

def save_user_access():
    with open("user_access.pkl", "wb") as f:
        pickle.dump(dict(user_access), f)

def get_user_access(user_id: int) -> str:
    return user_access[user_id]

def set_user_access(user_id: int, access: str, update: Update):
    user_access[user_id] = access
    if update.message.from_user.username:
        print("@" + update.message.from_user.username + " reached access: " + access)

def user_access_keys():
    return user_access.keys()