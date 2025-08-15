from openai import OpenAI
from .Tokens import GEMMA_API_KEY

client = OpenAI(
    api_key=GEMMA_API_KEY,
    base_url="https://api.avalai.ir/v1",
)

def tldr_prompt(text: str) -> str:
    return f""" """ # insert tldr prompt here

def ai_summarize(text: str) -> str:
    prompt = tldr_prompt(text)

    response = client.chat.completions.create(
        model="gemma-3-27b-it",
        messages=[
            {"role": "user", "content": prompt}
        ],
        extra_body={"temperature": 0.5, "max_tokens": 250}
    )
    return response.choices[0].message.content.strip()

def ask_prompt(text: str, original_username: str = None, requester_username: str = None, bot_username: str = None) -> str:
    introduction = "" # optional
    if original_username and requester_username:
        if original_username == requester_username:
            introduction = f"User @{original_username} sent the message and requested a response."
        else:
            introduction = f"User @{original_username} sent the message , and @{requester_username} requested a response."
    elif original_username:
        introduction = f"User @{original_username} sent the message. (the requester has not set up a username for their account.)"
    elif requester_username:
        introduction = f"User @{requester_username} requested a response. (the original poster has not set up a username for their account.)"

    return f""" """ # insert ask prompt here

def ai_opinion(text: str, original_username: str = None, requester_username: str = None, bot_username: str = None) -> str:
    prompt = ask_prompt(text, original_username, requester_username)

    response = client.chat.completions.create(
        model="gemma-3-27b-it",
        messages=[
            {"role": "user", "content": prompt}
        ],
        extra_body={"temperature": 0.5, "max_tokens": 750}
    )

    content = response.choices[0].message.content
    return content.strip() if content else "خطا در دریافت پاسخ از هوش مصنوعی"