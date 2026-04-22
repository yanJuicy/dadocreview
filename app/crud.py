"""
[파일 역할]
이 파일은 데이터베이스(DB)에 데이터를 직접 읽고 쓰는 함수들을 모아놓은 곳입니다.
1. 데이터를 생성(Create), 조회(Read), 수정(Update), 삭제(Delete)하는 로직을 담당합니다.
2. 비즈니스 로직과 DB 연동 로직을 분리하여 코드의 재사용성을 높입니다.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Book
from . import schemas


def read_book_by_id(db: Session, book_id):
    stmt = select(Book).where(Book.id == book_id)
    result = db.execute(stmt)
    return result


def search_books_by_title(db: Session, title: str):
    stmt = select(Book).where(Book.title.contains(title))
    result = db.execute(stmt)
    return result.scalars().all()


# app/crud.py 내부의 create_book 수정 방향
def create_book(db: Session, book_data: dict):  # schemas.Book 대신 dict로 받기
    db_book = Book(
        title=book_data.get("title"),
        author=book_data.get("author"),
        isbn=book_data.get("isbn"),
        cover_image_url=book_data.get("cover_image_url"),
        # 나머지 필드들도 .get()으로 처리하거나 기본값 설정
        description=book_data.get("description", ""),
        kyobo_link=book_data.get("kyobo_link", ""),
        yes24_link=book_data.get("yes24_link", ""),
        aladin_link=book_data.get("aladin_link", ""),
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def sync_books(db: Session, books_data: list):
    for book in books_data:
        isbn = book.get("isbn")

        stmt = select(Book).where(Book.isbn == isbn)
        existing_book = db.execute(stmt).scalar_one_or_none()

        if not existing_book:
            create_book(db, book)
