from dotenv import load_dotenv
from fastapi import APIRouter
from openai import OpenAI
import os
import requests

router = APIRouter(prefix="/api/v1")


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


@router.post("/generate_concepts")
async def gpt_api(message):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You will be asked to enter some topic from the user." 
                                          "All you have to do is recommend four logo design concepts that fit that theme." 
                                          "In Korean."},
            {"role": "user", "content": message}
        ]
    )
    return completion.choices[0].message

def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f'Image successfully downloaded: {save_path}')
    else:
        print('Failed to download image')

@router.post("/generate_logo")
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

    image_url = logo_url
    save_path = 'images/test2.png'  # 예: 'downloaded_image.jpg'
    download_image(image_url, save_path)

    return logo_urls