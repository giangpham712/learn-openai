import traceback
import openai
from .transcriber import Transcriber


prompts = {
        "START": "Classify the intent of one next input. \
             Is it: WRITE_EMAIL, QUESTION, OTHER ? Only answer one word.",
        "QUESTION": "If you can answer the question: ANSWER, \
                 if you need more information: MORE, \
                 if you cannot answer: OTHER. Only answer one word.",
        "ANSWER": "Now answer the question",
        "MORE": "Now ask for more information",
        "OTHER": "Now tell me you cannot answer the question or do the action",
        "WRITE_EMAIL": 'If the subject or recipient or message is missing, \
                   answer "MORE". Else if you have all the information, \
                   answer "ACTION_WRITE_EMAIL |\
                   subject:subject, recipient:recipient, message:message".',
    }

actions = {
    "ACTION_WRITE_EMAIL": "The mail has been sent. \
    Now tell me the action is done in natural language."
}

messages = [{"role": "user", "content": prompts["START"]}]

def run(file):
    try:
        transcriber = Transcriber()
        input = transcriber.transcribe(file)
        return start(input)
    except Exception as e:
        return f"{traceback.format_exc()}"

def start(user_input):
    messages = [{"role": "user", "content": prompts["START"]}]
    messages.append({"role": "user", "content": user_input})
    return discussion(messages, "START")

def discussion(messages, last_step):
    answer = generate_answer(messages)
    print(answer)
    if answer in prompts.keys():
        messages.append({"role": "assistant", "content": answer})
        messages.append({"role": "user", "content": prompts[answer]})
        return discussion(messages, answer)
    elif answer.split("|")[0].strip() in actions.keys():
        do_action(answer)
    else:
        if last_step != 'MORE':
            messages=[]
        last_step = 'END'
        return answer

def do_action(answer):
    print("Doing action " + answer)
    messages.append({"role": "assistant", "content": answer})
    action = answer.split("|")[0].strip()
    messages.append({"role": "user", "content": actions[action]})
    return discussion(messages, answer)

def generate_answer(messages):
    print(messages)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )
    return response.choices[0].message.content
