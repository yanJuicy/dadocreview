"""
[파일 역할]
이 파일은 전체 웹 서버 애플리케이션의 실행 지점이자 컨트롤 타워 역할을 합니다.
1. FastAPI 애플리케이션 객체를 생성하고 관리합니다.
2. 각 웹 주소(URL) 요청과 처리 함수를 연결(Routing)합니다.
3. 서버가 시작될 때 필요한 초기화 작업(DB 테이블 생성 등)을 수행합니다.
"""

from app import crud
from fastapi import Depends
from sqlalchemy.orm import Session
from app import schemas
from fastapi import FastAPI
from .database import engine, SessionLocal
from . import models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# models.py에 있는 내용을 보고 DB 테이블을 만든다
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Dadoc Review!"}


@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.Book, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
