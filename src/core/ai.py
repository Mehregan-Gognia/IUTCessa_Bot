from langchain.chat_models import init_chat_model
from .setting import GEMMA_API_KEY

client = init_chat_model(
    base_url="https://api.avalai.ir/v1", 
    api_key=GEMMA_API_KEY,
    model="gpt-5-nano-2025-08-07",
    model_provider="openai",
    temperature=0.5,
    max_tokens=300
)

def tldr_prompt(text: str, is_bot_being_summarized: bool = False) -> str:
    def summarizing_oneself(is_it_tho: bool) -> str:
        return "Impotant note:\nThe message you are given to summarize is a message that you sent previously. *You are summarizing your own message right now.*" if is_it_tho else ""

    return f""" """ # <- Insert tldr prompt here

def ai_summarize(text: str, is_bot_being_summarized: bool = False) -> str:
    prompt = tldr_prompt(text= text, is_bot_being_summarized=is_bot_being_summarized)

    response = client.invoke(prompt)
    return response.content.strip()

def ask_prompt(
            text: str, requester_note: str = None,
            original_username: str = None, requester_username: str = None, bot_username: str = None
            )-> str:
    def format_username(username):
        return f"@{username}" if username else "*an unknown user*"
    
    introduction = ""
    if original_username and requester_username:
        if original_username == requester_username:
            introduction = f"User {format_username(original_username)} sent the original message and also requested a response."
        else:
            introduction = f"User {format_username(original_username)} sent the original message, and {format_username(requester_username)} requested a response."
    elif original_username:
        introduction = f"User {format_username(original_username)} sent the original message. (the requester has no username)"
    elif requester_username:
        introduction = f"User {format_username(requester_username)} requested a response. (the original poster has no username)"

    note_section = f"\nThe requester ({format_username(requester_username)}) added this note: \"{requester_note}\"" if requester_note else "\nThe requester was null, so you're giving opinion on the original message now (You can mention the requester *only if needed*)"

    return f""" """ # <- Insert ask prompt here

def ai_opinion(
            text: str, requester_note: str = None,
            original_username: str = None, requester_username: str = None, bot_username: str = None
            )-> str:
    prompt = ask_prompt(text= text, requester_note= requester_note,
                        original_username= original_username, requester_username= requester_username, 
                        bot_username= bot_username)

    response = client.invoke(prompt)

    content = response.content
    return content.strip() if content else "Error receiving response from AI"