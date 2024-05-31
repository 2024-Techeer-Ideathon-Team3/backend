import os
from dotenv import load_dotenv
import fastapi
from fastapi import FastAPI
from routes import router
import openai

app = FastAPI()

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(router)
