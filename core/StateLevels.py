from telegram import Update
from collections import defaultdict
import pickle

USER_STATES = { # FSM (for user state)
    "main-menu",
    "kmk-yar-main", "kmk-yar-get-link",
    "tech-stack-main", "tech-stack-first-forum", "tech-stack-user-info-confirm",
    "tech-stack-decision", "tech-stack-see-info", "tech-stack-pay",
    "backdoor-panel-head", "backdoor-panel", "backdoor-access-denied" ,
    "admin-list", "admin-add", "admin-remove",
    "registrant-panel", "registrant-edit", "registrant-edit-input", "registrant-remove", "registrant-remove-confirm",
    "interview-panel", "interviewee-accept", "interviewee-remove", "interviewee-reject",
    "pay-panel", "pay-list", "payer-add", "payer-remove",
    "filter-panel", "message-panel", "broadcast-confirm", "search-choose", "search-confirm", "user-search",
    "uploading-stage",
    "tach-stack-remind", "remind-add", "remind-remove"
}

KMKYAR_MENUS = {
    "kmk-yar-main", "kmk-yar-get-link"
}

TECH_STACK_USER_PANEL = {
    "tech-stack-main", "tech-stack-first-forum", "tech-stack-user-info-confirm",
    "tech-stack-decision", "tech-stack-pay",
    "tach-stack-remind", "remind-add", "remind-remove"
}

TECH_STACK_ADMIN_PANEL = {
    "backdoor-panel-head", "backdoor-panel", "backdoor-access-denied" ,
    "admin-list", "admin-add", "admin-remove",
    "registrant-panel", "registrant-edit", "registrant-edit-input", "registrant-remove", "registrant-remove-confirm",
    "interview-panel", "interviewee-accept", "interviewee-remove", "interviewee-reject",
    "pay-panel", "pay-list", "payer-add", "payer-remove",
    "uploading-stage",
    "filter-panel", "message-panel", "broadcast-confirm", "search-choose", "search-confirm", "user-search"    
}

user_states = defaultdict(lambda: "main-menu") #default state

def load_user_state():
    global user_states
    try:
        with open("user_states.pkl", "rb") as f:
            user_states = defaultdict(lambda: "main-menu", pickle.load(f))
        print("User states loaded successfully.")
    except FileNotFoundError:
        print("No existing state file found. Starting fresh.")
        user_states = defaultdict(lambda: "main-menu")

def save_user_state():
    with open("user_states.pkl", "wb") as f:
        pickle.dump(dict(user_states), f)

def get_user_state(user_id: int) -> str:
    return user_states[user_id]

def set_user_state(user_id: int, state: str, update: Update):
    user_states[user_id] = state
    if update.message.from_user.username:
        print("@" + update.message.from_user.username + " reached state: " + state)