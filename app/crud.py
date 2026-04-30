"""
[파일 역할]
이 파일은 데이터베이스(DB)에 데이터를 직접 읽고 쓰는 함수들을 모아놓은 곳입니다.
1. 데이터를 생성(Create), 조회(Read), 수정(Update), 삭제(Delete)하는 로직을 담당합니다.
2. 비즈니스 로직과 DB 연동 로직을 분리하여 코드의 재사용성을 높입니다.
"""

from app.models import Library
from app.models import Review
from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Book
from . import schemas


def read_book_by_id(db: Session, book_id):
    stmt = select(Book).where(Book.id == book_id)
    return db.execute(stmt).scalar_one_or_none()


def search_books_by_title(db: Session, title: str, limit: int, offset: int):
    stmt = select(Book).where(Book.title.contains(title)).offset(offset).limit(limit)
    result = db.execute(stmt)
    return result.scalars().all()


# app/crud.py 내부의 create_book 수정 방향
def create_book(db: Session, book_data: dict):  # schemas.Book 대신 dict로 받기
    db_book = Book(
        title=book_data.get("title"),
        author=book_data.get("author"),
        isbn=book_data.get("isbn"),
        publisher=book_data.get("publisher"),
        publication_year=book_data.get("publication_year"),
        loan_count=book_data.get("loan_count", 0),
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


def sync_reviews(db: Session, book_id: str, reviews_data: list):

    stmt = select(Book).where(Book.id == book_id)
    find_book = db.execute(stmt).scalar_one_or_none()

    if not find_book:
        return

    existing_review_ids = [review.source_review_id for review in find_book.reviews]

    for review in reviews_data:
        source_id = review.get("source_review_id", "")
        if source_id in existing_review_ids:
            continue

        book_review = Review(
            book_id=find_book.id,
            rating=review.get("rating"),
            content=review.get("content"),
            source_url=review.get("source_url", ""),
            source_site=review.get("source_site", ""),
            source_review_id=review.get("source_review_id", ""),
        )
        db.add(book_review)

    db.commit()



def search_libraries(db: Session, library_name: str):
    stmt = select(Library).where(Library.name.contains(library_name))
    result = db.execute(stmt)
    return result.scalars().all()