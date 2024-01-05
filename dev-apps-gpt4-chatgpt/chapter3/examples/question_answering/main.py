from .data_service import DataService
from .intent_service import IntentService
from .response_service import ResponseService

def run(question: str, file: str):
    data_service = DataService()
    data = data_service.pdf_to_embeddings(file)
    data_service.load_data_to_redis(data)

    intent_service = IntentService()
    intents = intent_service.get_intent(question)

    facts = data_service.search_redis(intents)
    response_service = ResponseService()

    answer = response_service.generate_response(facts, question)
    print(answer)