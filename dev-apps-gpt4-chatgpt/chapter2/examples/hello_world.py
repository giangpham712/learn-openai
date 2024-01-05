import openai

def run():
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello World!"}],
    )
    print(response.model_dump_json())