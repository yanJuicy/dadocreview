"""
[파일 역할]
이 파일은 Pydantic 라이브러리를 사용하여 데이터의 '검증' 및 '입출력 규격'을 정의합니다.
1. 사용자가 보낸 데이터가 올바른 형식인지 확인합니다. (Validation)
2. API 응답으로 내보낼 데이터의 항목을 제어합니다. (Serialization)
"""

from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    description: str
    cover_image_url: str
    average_review_score: float
    review_count: int
    ai_review_pro: str
    ai_review_con: str
    book_index: str
    kyobo_link: str
    yes24_link: str
    aladin_link: str
    model_config = ConfigDict(from_attributes=True)
