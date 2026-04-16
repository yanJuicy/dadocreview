"""
[파일 역할]
이 파일은 전체 웹 서버 애플리케이션의 실행 지점이자 컨트롤 타워 역할을 합니다.
1. FastAPI 애플리케이션 객체를 생성하고 관리합니다.
2. 각 웹 주소(URL) 요청과 처리 함수를 연결(Routing)합니다.
3. 서버가 시작될 때 필요한 초기화 작업(DB 테이블 생성 등)을 수행합니다.
"""

from app.services import naru_api
from app import crud
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app import schemas
from fastapi import FastAPI
from .database import engine, SessionLocal
from . import models
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# models.py에 있는 내용을 보고 DB 테이블을 만든다
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/results", response_class=HTMLResponse)
def read_results(request: Request, q: str = None, db: Session = Depends(get_db)):
    # q는 검색창에 입력한 키워드(ex: /results?q=파이썬)

    external_books = naru_api.fetch_books_from_naru(q)
    print(external_books)

    books = crud.search_books_by_title(db=db, title=q)

    return templates.TemplateResponse(
        request, "results.html", {"keyword": q, "books": external_books}
    )


@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.Book, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
