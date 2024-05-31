from dotenv import load_dotenv
from fastapi import APIRouter
from openai import OpenAI
import os
from typing import List, Optional
from pydantic import BaseModel



router = APIRouter(prefix="/api/v1")


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class LogoDesign(BaseModel):
    concept: str
    explanation: str
    elements: List[str]

def parse_logo_designs(content: str):
    lines = content.split("\n")
    designs = []
    current_design = {}

    for line in lines:
        if line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4."):
            if current_design:
                # 현재 디자인을 리스트에 추가하고 새 디자인을 시작
                designs.append(LogoDesign(**current_design))
                current_design = {}
            # 컨셉 추출
            concept = line.split("**")[1]
            current_design['concept'] = concept
        elif "**설명**:" in line:
            # 설명 추출
            explanation = line.split(":")[1].strip()
            current_design['explanation'] = explanation
        elif "**요소**:" in line:
            # 요소 추출
            elements = line.split(":")[1].split(",")
            elements = [element.strip() for element in elements]
            current_design['elements'] = elements

    # 마지막 디자인 추가
    if current_design:
        designs.append(LogoDesign(**current_design))

    return {"designs": designs}


@router.post("/generate_concepts")
async def gpt_api(topic):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are tasked with receiving a project concept from the user and recommending logo design concepts that fit the project."
                                          "SPECIFICALLY Recommend 4 logo design concepts by focusing on the object and verb of the user’s input and explain what each concept means."
                                          "List the elements that go into each design as nouns."
                                          "Respond in Korean."
                                          },
                                        
            {"role": "user", "content": f"{topic}. PLEASE RECOMMEND LOGO DESIGNS BY FOCUSING ON THE OBJECT AND VERB OF THE MY INPUT."},
            
        ],
        
    )
    response_text = completion.choices[0].message.content
    return parse_logo_designs(response_text)

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