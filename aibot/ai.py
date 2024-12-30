from functools import lru_cache

from llama_index.core import Settings, VectorStoreIndex
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.vector_stores.upstash import UpstashVectorStore

import google.generativeai as genai

import helpers

GOOGLE_GEMINI_API_KEY = helpers.config("GOOGLE_GEMINI_API_KEY", default = None)
UPSTASH_VECTOR_URL = helpers.config("UPSTASH_VECTOR_URL", default = None)
UPSTASH_VECTOR_TOKEN = helpers.config("UPSTASH_VECTOR_TOKEN", default = None)

@lru_cache
def get_vector_store_index():
    genai.configure(api_key = GOOGLE_GEMINI_API_KEY)

    Settings.llm = Gemini(model = "models/gemini-1.5-pro", api_key = GOOGLE_GEMINI_API_KEY)
    Settings.embed_model = GeminiEmbedding(model = "models/text-embedding-004", api_key = GOOGLE_GEMINI_API_KEY)

    vector_store = UpstashVectorStore(
        url = UPSTASH_VECTOR_URL,
        token = UPSTASH_VECTOR_TOKEN
    )

    return VectorStoreIndex.from_vector_store(vector_store = vector_store)

@lru_cache
def get_query_engine():
    index = get_vector_store_index()
    return index.as_query_engine()

def query(message):
    query_engine = get_query_engine()
    response = query_engine.query(message)

    return response

