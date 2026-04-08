"""
[파일 역할]
이 파일은 Pydantic 라이브러리를 사용하여 데이터의 '검증' 및 '입출력 규격'을 정의합니다.
1. 사용자가 보낸 데이터가 올바른 형식인지 확인합니다. (Validation)
2. API 응답으로 내보낼 데이터의 항목을 제어합니다. (Serialization)
3. DB 모델(SQLAlchemy)과 API 데이터 사이의 징검다리 역할을 합니다.
"""

from pydantic import BaseModel
from typing import Optional


class Book(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    description: str
    cover_image_url: Optional[str] = None
    average_review_score: Optional[float] = None
    review_count: Optional[int] = None
    ai_review_pro: Optional[str] = None
    ai_review_con: Optional[str] = None
    book_index: Optional[str] = None
    kyobo_link: str
    yes24_link: str
    aladin_link: str
