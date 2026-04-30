"""
[파일 역할]
엑셀파일을 읽어와서 데이터베이스에 저장

[사용법]
python scripts/import_libraries.py

"""

import pandas as pd

from app.database import SessionLocal
from app.models import Library
from app.database import engine, Base

def import_libraries_from_excel(file_path: str):
    Base.metadata.create_all(bind=engine)

    try:
        df = pd.read_excel(file_path, header=7)
    except FileNotFoundError:
        print(f"Error: 파일을 찾을 수 없습니다. {file_path}")
        return

    db = SessionLocal()

    for _, row in df.iterrows():
        library = Library(
            name=row['도서관명'],
            address=row['주소'],
            phone=row['전화번호'],
            closed_days_info=row['휴관일'],
            latitude=row['위도'],
            longitude=row['경도'],
            lib_code=row['도서관코드'],
            homepage=row['홈페이지']
        )
        db.add(library)

    db.commit()
    db.close()

if __name__ == "__main__":
    import_libraries_from_excel("data/libraries.xlsx")
