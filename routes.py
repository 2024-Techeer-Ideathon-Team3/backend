from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
import os
import openai

router = APIRouter(prefix="/api/v1")

app = FastAPI()

@app.post("/generate-image")
async def generate_image(prompt: str):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return {"image_url": response['data'][0]['url']}
