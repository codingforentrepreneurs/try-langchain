from decouple import config
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import UpstashVectorStore
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

OPENAI_API_KEY = config("OPENAI_API_KEY")
UPSTASH_VECTOR_REST_URL = config("UPSTASH_VECTOR_REST_URL")
UPSTASH_VECTOR_REST_TOKEN = config("UPSTASH_VECTOR_REST_TOKEN")

LLM_CONFIG = {
    "model": "gpt-4o-mini",
    "api_key": OPENAI_API_KEY
}


embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = UpstashVectorStore(
    embedding=embeddings,
    index_url=UPSTASH_VECTOR_REST_URL,
    index_token=UPSTASH_VECTOR_REST_TOKEN
)

llm = ChatOpenAI(**LLM_CONFIG)


message = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""

prompt = ChatPromptTemplate.from_messages([("human", message)])

retriever = store.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 2}
)

parser = StrOutputParser()


def get_chain():
    return {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | parser





