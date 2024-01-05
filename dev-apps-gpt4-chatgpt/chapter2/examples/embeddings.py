import openai


def run():
    response = openai.embeddings.create(
        model="text-embedding-ada-002", input="your text"
    )

    print(response.model_dump_json(indent=2))
