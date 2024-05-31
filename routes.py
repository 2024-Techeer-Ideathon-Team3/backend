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
    capture_mode = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 블록 시작을 감지 (숫자로 시작하는 경우)
        if line[0].isdigit() and '.' in line:
            # 이전 디자인 저장
            if current_design:
                # 모든 필수 정보가 있는지 검증
                if 'concept' in current_design and 'explanation' in current_design and 'elements' in current_design:
                    designs.append(LogoDesign(**current_design))
                current_design = {}
            # 컨셉 추출
            concept_part = line.split('.', 1)[1]  # 첫 번째 점 이후 모든 텍스트
            concept = concept_part.split(':', 1)[0].strip()  # 첫 번째 콜론 이전까지의 텍스트
            current_design['concept'] = concept
            capture_mode = None

        # 설명이나 요소 추출
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if "의미" in key:
                current_design['explanation'] = value
                capture_mode = 'explanation'
            elif "설명" in key:
                current_design['explanation'] = value
                capture_mode = 'explanation'
            elif "요소" in key:
                elements = [elem.strip() for elem in value.split(',')]
                current_design['elements'] = elements
                capture_mode = 'elements'
            elif "구성 요소" in key:
                elements = [elem.strip() for elem in value.split(',')]
                current_design['elements'] = elements
                capture_mode = 'elements'

    # 마지막 디자인 저장
    if current_design and 'concept' in current_design and 'explanation' in current_design and 'elements' in current_design:
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
                                          "List the elements that go into each design as nouns. But don't mention the color"
                                          "Respond in Korean."
                                          },
                                        
            {"role": "user", "content": f"{topic}. PLEASE RECOMMEND LOGO DESIGNS BY FOCUSING ON THE OBJECT AND VERB OF THE MY INPUT."},
            
        ],
        
    )
    response_text = completion.choices[0].message.content
    print(response_text)
    return parse_logo_designs(response_text)

class LogoRequest(BaseModel):
    explanation: str
    elements: list[str]
    colorCode: str

@router.post("/generate_logos")
async def dalle_api(request: LogoRequest):
    client = OpenAI(api_key=api_key)
    logo_urls = []
    prompt = f"design a simple logo according to the following sentences: {request.explanation} with elements {', '.join(request.elements)} in color {request.colorCode}"
    for i in range(4):
        url_response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        # 생성된 이미지의 URL 추출
        logo_url = str(url_response.data[0].url)  # 이미지 url 출력
        logo_urls.append(logo_url)

    return logo_urls