import openai

def run():
    response = openai.moderations.create(model="text-moderation-latest", input="I want to kill my neighbor.")
    print(response.model_dump_json(indent=2))