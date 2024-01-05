import openai

def run():
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful teacher."},
            {
                "role": "user",
                "content": "Are there other measures than time complexity for an \
                            algorithm?",
            },
            {
                "role": "assistant",
                "content": "Yes, there are other measures besides time complexity \
                            for an algorithm, such as space complexity.",
            },
            {"role": "user", "content": "What is it?"},
        ],
        n=1
    )

    print(response.model_dump_json())