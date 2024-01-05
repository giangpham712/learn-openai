import openai
from typing import List

prompt_role = ("You are an assistant for journalists. "
               "Your task is to write articles, based on the FACTS that are given to you. "
               "You should respect the instrutions: the TONE. the LENGTH, and the STYLE")

def ask_chatgpt(messages):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )
    return response.choices[0].message.content

def assist_journalist(
        facts: List[str], tone: str, length_words: int, style: str
):
    facts = ", ".join(facts)
    prompt = f"{prompt_role} \
        FACTS: {facts} \
        TONE: {tone} \
        LENGTH: {length_words} words \
        STYLE: {style}"
    return ask_chatgpt([{"role": "user", "content": prompt}])