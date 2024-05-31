from dotenv import load_dotenv
from fastapi import APIRouter
from openai import OpenAI
import os

router = APIRouter(prefix="/api/v1")


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")



@router.post("/generate_logo")
async def dalle_api(message):
    client = OpenAI(api_key=api_key)

    url_response = client.images.generate(
        model="dall-e-3",
        prompt=message,
        n=1,
        size="1024x1024"
    )

    # 생성된 이미지의 URL 추출
    logo_url = str(url_response.data[0].url)  # 이미지 url 출력

    return logo_url