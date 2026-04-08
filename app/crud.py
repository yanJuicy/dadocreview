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


def create_book(db: Session, book: schemas.Book):
    db_book = Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        description=book.description,
        cover_image_url=book.cover_image_url,
        average_review_score=book.average_review_score,
        review_count=book.review_count,
        ai_review_pro=book.ai_review_pro,
        ai_review_con=book.ai_review_con,
        book_index=book.book_index,
        kyobo_link=book.kyobo_link,
        yes24_link=book.yes24_link,
        aladin_link=book.aladin_link,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
