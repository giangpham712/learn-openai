import openai

def summarize_transcript(transcript):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Summarize the following text"},
            {"role": "assistant", "content": "Yes."},
            {"role": "user", "content": transcript},
        ]
    )
    print(response.choices[0].message.content)