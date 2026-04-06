"""
[파일 역할]
이 파일은 데이터베이스(DB) 내부에 어떤 형태의 표(Table)를 만들지 정의하는 설계도 역할을 합니다.
1. 'Book', 'Review' 등 실제 저장할 데이터의 항목(Column)을 규정합니다.
2. 각 데이터 타입(숫자, 문자, 날짜 등)을 정확히 지정합니다.
3. 서로 다른 표 사이의 논리적 연결 고리(관계)를 설정합니다.
"""

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

book_library = Table(
    "book_library",  # 데이터베이스에 만들어질 실제 표의 이름
    Base.metadata,  # 우리 데이터베이스 설계도(Base)에 등록합니다.
    # 1. 책 번호를 적는 칸 (ForeignKey: 'books' 테이블의 'id'를 가리킵니다.)
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    # 2. 도서관 번호를 적는 칸 (ForeignKey: 'libraries' 테이블의 'id'를 가리킵니다.)
    Column("library_id", ForeignKey("libraries.id"), primary_key=True),
)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    isbn = Column(String, unique=True, index=True)
    description = Column(Text)
    cover_image_url = Column(String)
    average_review_score = Column(Float)
    review_count = Column(Integer)
    ai_review_pro = Column(String)
    ai_review_con = Column(String)
    book_index = Column(Text)
    kyobo_link = Column(String)
    yes24_link = Column(String)
    aladin_link = Column(String)

    # "이미지 한 장당 리뷰 여러 개" 라고 관계를 맺어줍니다.
    reviews = relationship("Review", back_populates="book")
    # "책과 도서관 사이의 연결 장부(book_library)를 사용해라" 라고 알려줍니다. (N:N)
    libraries = relationship("Library", secondary=book_library, back_populates="books")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    rating = Column(Integer)
    content = Column(Text)
    source_url = Column(String)
    source_site = Column(String)
    source_review_id = Column(String)

    # "이 리뷰가 소속된 책 한 권"을 가리킵니다. (1:1 느낌)
    book = relationship("Book", back_populates="reviews")


class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    phone = Column(String)
    closed_days_info = Column(String)
    library_code = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

    # "이 도서관이 보유한 책들"을 연결 장부를 통해 가져옵니다. (N:N)
    books = relationship("Book", secondary=book_library, back_populates="libraries")
