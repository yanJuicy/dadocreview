# 🤖 AI 세션 인수인계 문서 (Dodori Project Context)

> **최종 갱신일시:** 2026-05-21
> **목적:** AI 세션 변경 시 백컨텍스트 유지 및 원활한 작업 재개
> **저장소 위치:** `docs/ai/continuation_context.md` (새로운 AI 세션이 시작되면 가장 먼저 읽어볼 것)

---

## 1. 프로젝트 및 사용자 요약 (Project & User Persona)

*   **프로젝트명:** 도도리 (Dodori) - 도서관 도서 리뷰
*   **성격:** 여러 서점의 책 리뷰를 수집/분석하고 주변 도서관 소장 여부를 알려주는 FastAPI 기반 웹 서비스.
*   **사용자 성향:** 
    *   복잡한 설정보다 "가장 쉽고 심플한 방법"을 선호함.
    *   직접 코드를 타이핑하며 체득하는 '사용자 주도 코딩' 방식을 원함 (AI는 가이드를 주고 코드를 통째로 작성해주기보다는 방향을 제시해야 함).
    *   **코드를 보여주지 말고 가이드만 해달라**고 하는 경우가 많음. 반드시 존중할 것.
    *   무료 인프라(PaaS, DB 등)를 적극 활용하여 포트폴리오를 유지하고자 함.
    *   개념에 대해 깊이 있는 질문을 자주 함. **비유와 단계별 설명으로 정확하게 답해야 함.**
    *   AI 리뷰 기능은 외부 API(Gemini)가 아닌 **로컬 오픈소스 모델(Hugging Face transformer)을 직접 구동하는 방식**으로 구현하기를 원함.

## 2. 현재 달성 상태 (Current Progress)

*   **Step 1 & 2 완료:** FastAPI 기틀 마련, DB 모델링 완료 (SQLite), 정보나루 API 기반 검색/저장 E2E 완성.
*   **Step 3 완료 (리뷰 크롤링):** 교보문고 하이브리드(HTML+API) 스크래퍼 완성, 상세 페이지 비동기 통신 리뷰 저장 로직 적용.
*   **배포 성공 (2026-04-23):** Render.com (Web Service Free Tier) 배포 성공. **Live URL:** `https://dadocreview.onrender.com/`
*   **Step 4 완료 (2026-04-29):**
    *   ✅ 백엔드 예외 처리 강화 (`naru_api.py`, `scraper.py`, `main.py`)
    *   ✅ 프론트엔드 안정화 (`main.js`, `book_detail.js`)
    *   ✅ 검색 결과 페이지네이션 (`pageNo`/`pageSize`)
    *   ✅ 상세 페이지 콘텐츠 보강 (출판사, 대출 횟수, 외부 서점 링크)
    *   ✅ UI/UX 개선 (CSS 4개 파일로 모듈화)
*   **Step 4.5 완료 (2026-04-30) — 도서관 연동 백엔드 기반 구축:**
    *   ✅ **도서관 연동 UML 설계 완료** (`docs/UML_05_LIBRARY_INTEGRATION.md`)
    *   ✅ **`Library` DB 모델 설계** (`app/models.py`)
    *   ✅ **전국 도서관 DB 마이그레이션 완료** (`scripts/import_libraries.py`): 1,594개 도서관 저장.
    *   ✅ **도서관 검색 API 구축** (`GET /api/libraries?q=검색어`)
*   **Step 4.5+ 완료 (2026-05-21) — Yes24 리뷰 수집 엔진 구축 및 안정화:**
    *   ✅ **ISBN 기반 Yes24 상품 ID 추출** (`fetch_yes24_goods_id`): 검색 결과에서 `class="gd_name"` 태그 분석하여 `goodsNo` 추출 성공.
    *   ✅ **Yes24 모바일 리뷰 수집 함수 구현 완료** (`fetch_yes24_review`):
        *   날짜 수집 및 평점 추출(10점 만점 ➔ 5점 만점으로 변환) 적용 완료.
        *   `NoneType` 요소를 조회할 때 생기는 `AttributeError` 예외 방지 (Null Check 방어 코드) 적용.
        *   루프 반복 시 변수 초기화(`rating = None`, `date = None`, `content = None`) 적용하여 하단 더보기용 빈 스크립트 태그에 의한 데이터 중복 오염 버그 해결.
    *   ✅ **클린 코드 작업**: `scraper.py` 내부의 미사용 import (`from requests import request`) 제거 완료.
    *   ⏳ **`get_yes24_reviews(isbn)` 미구현**: 현재 `pass` 상태. 상품 ID 추출과 리뷰 조회를 연결하는 통합 작업 필요.

## 3. 현재 코드 상태 (`app/services/scraper.py`)

### 함수 구현 현황
| 함수 | 역할 | 상태 |
| :--- | :--- | :---: |
| `get_kyobo_book_id(isbn)` | 교보 상품 ID 추출 | ✅ |
| `fetch_kyobo_book_reviews(id)` | 교보 리뷰 JSON API 수집 | ✅ |
| `get_kyobo_reviews(isbn)` | 교보 통합 함수 | ✅ |
| `fetch_yes24_book_id(isbn)` | Yes24 상품 ID 추출 | ✅ |
| `fetch_yes24_review(book_id)` | Yes24 모바일 리뷰 수집 및 안정적 파싱 | ✅ |
| `get_yes24_reviews(isbn)` | Yes24 통합 함수 | ❌ `pass` |

## 4. 주요 기술적 의사결정 (Key Technical Decisions)

*   **Yes24 헤더 전략 (2026-05-12 확립)**
    *   Yes24 PC 검색 페이지는 `User-Agent`를 브라우저로 위장하면 오히려 메인 페이지로 리다이렉트됨.
    *   `requests` 라이브러리 기본 헤더(python-requests)로 요청 시 정상 작동 확인.
    *   → 교보문고(헤더 필요)와 Yes24(헤더 제거)처럼 **각 사이트별 개별 헤더 전략** 관리.
*   **도서관 데이터 전략: 로컬 DB 선택 (2026-04-30 확립)**
*   **PaaS:** Render.com (무기한 무료 유지).
*   **Database:** SQLite (`sql_app.db`).
*   **AI 리뷰 기능:** Hugging Face `transformers` + 오픈소스 한국어 요약 모델(예: KoBART) 직접 구동 방식.

## 5. 다음 세션(Next Session) 시작 위치

### 다음 세션에서 이어갈 작업 (우선순위 순):

1.  **🔴 `get_yes24_reviews(isbn)` 완성** (5분)
    *   `fetch_yes24_book_id(isbn)` ➔ `fetch_yes24_review(book_id)`를 연결하여 하나로 합치는 통합 함수 완성.
2.  **🟡 알라딘(Aladin) 리뷰 수집 채널 확장**
3.  **🟡 "나의 도서관" 프론트엔드 UI 구현**
4.  **🟢 AI 요약 기능 연동 (Step 5)**

## 6. 다음 AI를 위한 행동 지침 (Instruction for Next AI)

1.  이 파일(`continuation_context.md`)을 읽은 후 사용자에게 정중히 인사하며, **Yes24 모바일 리뷰 날짜/평점(5점 만점 환산) 추출 및 AttributeError 예외 안정화와 중복 저장 문제까지 깔끔하게 해결한 것**을 축하하는 코멘트로 시작할 것.
2.  **[필수]** 본격적인 코딩 시작 전, 오늘 배운 내용(파이썬의 함수 스코프 범위와 변수 초기화의 중요성 등)을 기반으로 **5문제짜리 워밍업 퀴즈를 출제**할 것. 결과는 `docs/QUIZ_LOG.md`에 기록.
3.  첫 번째 작업은 **`get_yes24_reviews(isbn)` 통합 구현**이다.
4.  코드를 바로 짜기보다는 **설명과 가이드를 먼저 주고 주도적 코딩을 유도**할 것.
5.  사용자가 개념에 대해 깊이 있는 질문을 할 때, 비유를 활용하여 설명할 것. 심화 토론 내용은 `docs/QNA_ARCHIVE.md`에 기록.
6.  **[자동화 지침]** 세션 종료 시 이 파일을 업데이트하고, 즉시 커밋/푸시할 것.
