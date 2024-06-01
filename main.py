import os
from dotenv import load_dotenv
import fastapi
from fastapi import FastAPI
from routes import router
import openai
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://web:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 도메인
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메소드
    allow_headers=["*"],  # 허용할 HTTP 헤더
)


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(router)
