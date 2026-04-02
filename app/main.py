# fastapi 라이브러리에서 FastAPI라는 클래스를 가져옵니다.
from fastapi import FastAPI

# FastAPI 클래스의 인스턴스(객체)를 생성합니다. 
# 이 변수가 웹 서버 전체를 관리하고 제어하는 역할을 합니다.
app = FastAPI()

# @ 기호는 데코레이터라고 부릅니다. 
# 브라우저에서 "/" 경로(기본 주소)로 들어오면(GET 요청), 바로 아래 함수를 실행하라는 뜻입니다.
@app.get("/")
def home():
    # 함수가 실행되면 브라우저에 딕셔너리(JSON) 형태의 데이터를 결과값으로 돌려줍니다.
    return {"message": "다독리뷰 서버 시동 완료!"}
