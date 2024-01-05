import openai
import json


def find_product(sql_query):
    results = [
        {"name": "pen", "color": "blue", "price": 1.99},
        {"name": "pen", "color": "red", "price": 1.78},
    ]
    return results


def run():
    functions = [
        {
            "name": "find_product",
            "description": "Get a list of products from a sql query",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": "A SQL query",
                    }
                },
                "required": ["sql_query"],
            },
        }
    ]

    user_question = "I need the top 2 products where the price is less than 2.00"
    messages = [{"role": "user", "content": user_question}]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0613", messages=messages, functions=functions
    )

    print(response.model_dump_json(indent=2))

    response_message = response.choices[0].message
    messages.append(response_message)

    function_name = response_message.function_call.name
    function_args = json.loads(response_message.function_call.arguments)
    products = find_product(function_args.get("sql_query"))

    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": json.dumps(products),
        }
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages
    )

    print(response.model_dump_json(indent=2))
