"""
[파일 역할]
이 파일은 외부 API인 '도서관 정보나루'와의 통신을 전담하는 서비스 레이어입니다.
1. 도서 검색, 상세 정보 조회 등 외부 API 호출 로직을 관리합니다.
2. 외부 API의 응답 데이터를 우리 시스템에 맞는 형식으로 정제하여 반환합니다.
3. API 키 관리(환경변수 활용) 및 통신 예외 처리를 담당합니다.
"""


import os
import requests
from dotenv import load_dotenv

load_dotenv()
NARU_API_KEY = os.getenv("NARU_API_KEY")


def fetch_books_from_naru(keyword: str):
    url = f"http://data4library.kr/api/srchBooks?authKey={NARU_API_KEY}&format=json&keyword={keyword}"
    response = requests.get(url)
    data =  response.json()

    raw_docs = data.get("response", {}).get("docs", [])

    books = []
    for item in raw_docs:
        doc = item.get("doc")

        refiend_book = {
            "title": doc.get("bookname"),
            "author": doc.get("authors"),
            "isbn": doc.get("isbn13"),
            "cover_image_url": doc.get("bookImageURL")
        }

        books.append(refiend_book)

    
    return books


