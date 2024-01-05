import numpy as np
import openai
import redis
from pypdf import PdfReader
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

INDEX_NAME = "embeddings-index"           # name of the search index
PREFIX = "doc"                            # prefix for the document keys
# distance metric for the vectors (ex. COSINE, IP, L2)
DISTANCE_METRIC = "COSINE"

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = ""


class DataService():
    def __init__(self):
        # Connect to Redis
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD
        )

    def pdf_to_embeddings(self, pdf_path: str, chunk_length: int = 1000):
        # Read data from pdf file and split it into chunks
        reader = PdfReader(pdf_path)
        chunks = []
        for page in reader.pages:
            text_page = page.extract_text()
            chunks.extend([text_page[i:i + chunk_length] for i in range(0, len(text_page), chunk_length)])

        # Create embeddings
        response = openai.embeddings.create(model='text-embedding-ada-002', input=chunks)
        return [{'id': value.index, 'vector': value.embedding, 'text': chunks[value.index]} for value in response.data]

    def load_data_to_redis(self, embeddings):
        try:
            self.redis_client.ft(INDEX_NAME).info()
            print("Index already exists")
        except:
            vector_dim = len(embeddings[0]['vector'])

            vector_number = len(embeddings)

            text = TextField(name="text")
            text_embedding = VectorField("vector", "FLAT", {
                "TYPE": "FLOAT32",
                "DIM": vector_dim,
                "DISTANCE_METRIC": "COSINE",
                "INITIAL_CAP": vector_number
            })
            fields = [text, text_embedding]

            self.redis_client.ft(INDEX_NAME).create_index(
                fields=fields,
                definition=IndexDefinition(
                    prefix=[PREFIX], index_type=IndexType.HASH
                )
            )

        for embedding in embeddings:
            key = f"{PREFIX}:{str(embedding['id'])}"
            embedding["vector"] = np.array(
                embedding["vector"], dtype=np.float32).tobytes()
            self.redis_client.hset(key, mapping=embedding)

        print(
            f"Loaded {self.redis_client.info()['db0']['keys']} documents in Redis search index with name: {INDEX_NAME}")

    def drop_redis_data(self, index_name: str = INDEX_NAME):
        try:
            self.redis_client.ft(index_name).dropindex()
            print('Index dropped')
        except:
            # Index doees not exist
            print('Index does not exist')

    def search_redis(self, user_query: str, index_name: str = "embeddings-index", vector_field: str = "vector",
                     return_fields: list = ["text", "vector_score"], hybrid_fields="*", k: int = 5,
                     print_results: bool = False):
        embedded_query = openai.embeddings.create(input=user_query, model="text-embedding-ada-002").data[0].embedding

        base_query = f'{hybrid_fields}=>[KNN {k} @{vector_field} $vector AS vector_score]'
        query = (
            Query(base_query).return_fields(*return_fields).sort_by("vector_score").paging(0, k).dialect(2)
        )
        params_dict = {"vector": np.array(embedded_query).astype(dtype=np.float32).tobytes()}

        results = self.redis_client.ft(index_name).search(query, params_dict)
        if print_results:
            for i, doc in enumerate(results.docs):
                score = 1 - float(doc.vector_score)
                print(f"{i}. {doc.text} (Score: {round(score, 3)})")

        return [doc.text for doc in results.docs]
