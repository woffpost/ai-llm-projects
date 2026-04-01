from fastapi import FastAPI
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import os

load_dotenv()

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

api_key = os.getenv("ANTHROPIC_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

client = ChatAnthropic(
    model="claude-opus-4-5",
    api_key="API KEY HERE", # To Do: разобраться почему ключ не подхватывается из переменных окружения, а только при явной передаче
    max_tokens=1024
)


# Загружаем каталог
with open("/Users/vladimirrusakov/Desktop/catalog.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

docs = [Document(page_content=line) for line in lines]
db = Chroma.from_documents(docs, embeddings)

# Модель запроса
class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    found_docs = db.similarity_search(query.question, k=3)
    context = "\n".join([doc.page_content for doc in found_docs])
    
    response = client.invoke([
        HumanMessage(content=f"Вот каталог моделей:\n{context}\n\nВопрос: {query.question}")
    ])
    
    return {"answer": response.content}

@app.post("/ask-stream")
async def ask_stream(query: Query):
    found_docs = db.similarity_search(query.question, k=3)
    context = "\n".join([doc.page_content for doc in found_docs])

    async def generate():
        for chunk in client.stream([
            HumanMessage(content=f"Каталог:\n{context}\n\nВопрос: {query.question}")
        ]):
            yield chunk.content

    return StreamingResponse(generate(), media_type="text/plain")