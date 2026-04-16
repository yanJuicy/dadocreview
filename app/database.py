"""
[파일 역할]
이 파일은 애플리케이션이 실제 데이터베이스(SQLite)와 통신하기 위한 설정을 관리합니다.
1. DB 파일의 저장 위치를 지정합니다.
2. 데이터 읽기/쓰기를 처리하는 엔진(Engine)을 생성합니다.
3. 데이터 작업을 실행할 세션(Session)을 제공하고 관리합니다.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. DB 파일 위치
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2. DB 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 데이터 작업을 실행할 세션 클래스
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 모든 모델의 부모가 될 Base 클래스
Base = declarative_base()
