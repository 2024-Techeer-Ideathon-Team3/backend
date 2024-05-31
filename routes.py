from dotenv import load_dotenv
from fastapi import APIRouter
from openai import OpenAI
import os

router = APIRouter(prefix="/api/v1")


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


@router.post("/generate_concepts")
async def gpt_api(topic):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You will be asked to enter some topic from the user."
                                          "Recommend 4 logo design concepts that fit the topic and what the concept means as content."
                                          "In concept, list as nouns what elements go into the design."
                                          "In Korean."},
            {"role": "user", "content": topic}
        ]
    )
    return completion.choices[0].message

@router.post("/generate_logos")
async def dalle_api(message):
    client = OpenAI(api_key=api_key)
    logo_urls = []
    for i in range(1):
        url_response = client.images.generate(
            model="dall-e-3",
            prompt=message,
            n=1,
            size="1024x1024"
        )
    # 생성된 이미지의 URL 추출
    logo_url = str(url_response.data[0].url)  # 이미지 url 출력
    logo_urls.append(logo_url)

    return logo_urls