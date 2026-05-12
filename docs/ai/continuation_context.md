# 🤖 AI 세션 인수인계 문서 (Dodori Project Context)

> **최종 갱신일시:** 2026-05-12
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
*   **Step 4.5+ 진행 중 (2026-05-12) — Yes24 리뷰 수집 엔진 구축:**
    *   ✅ **ISBN 기반 Yes24 상품 ID 추출** (`fetch_yes24_goods_id`): 검색 결과에서 `class="gd_name"` 태그 분석하여 `goodsNo` 추출 성공.
    *   ✅ **모바일 리뷰 엔드포인트 HTML 구조 분석 완료**: `m.yes24.com/Goods/ReviewList/{goods_id}` 경로의 `revwSet`, `total_rating_XX`, `revwCont` 클래스 구조 파악.
    *   ✅ **봇 감지 대응 전략 수립**: Header Paradox 발견 — Yes24 PC 검색은 `User-Agent` 헤더 없이(기본값) 접근해야 정상 작동.
    *   ⏳ **`fetch_yes24_review(goods_id)` 미구현**: 현재 `pass` 상태. 모바일 리뷰 파싱 로직 구현 필요.
    *   ⏳ **`get_yes24_reviews(isbn)` 미구현**: 현재 `pass` 상태. 두 함수 연결만 하면 됨.

## 3. 현재 코드 상태 (`app/services/scraper.py`)

### ⚠️ 정리 필요 사항 (다음 세션 시작 시 먼저 처리)
```
- 106행: print(soup)  ← 디버깅용, 제거 필요
- 112행: print(a_tag)  ← 디버깅용, 제거 필요
- 87-89행: 주석 처리된 User-Agent 헤더 코드 → 정리 필요
- 95행: 주석 처리된 이전 requests.get 호출 → 정리 필요
```

### 함수 구현 현황
| 함수 | 역할 | 상태 |
| :--- | :--- | :---: |
| `get_kyobo_book_id(isbn)` | 교보 상품 ID 추출 | ✅ |
| `fetch_kyobo_book_reviews(id)` | 교보 리뷰 JSON API 수집 | ✅ |
| `get_kyobo_reviews(isbn)` | 교보 통합 함수 | ✅ |
| `fetch_yes24_goods_id(isbn)` | Yes24 상품 ID 추출 | ✅ (디버그 print 잔존) |
| `fetch_yes24_review(goods_id)` | Yes24 모바일 리뷰 파싱 | ❌ `pass` |
| `get_yes24_reviews(isbn)` | Yes24 통합 함수 | ❌ `pass` |

### `fetch_yes24_review` 구현을 위한 분석 완료 사항
- **URL:** `https://m.yes24.com/Goods/ReviewList/{goods_id}?pageSize=10&pageNumber=1&sort_tp=2`
- **헤더:** 모바일 `User-Agent` 필요 (`Mozilla/5.0 (iPhone; ...`)
- **리뷰 컨테이너:** `<div class="revwSet" data-review-seq="...">`
- **평점:** `<span class="total_rating total_rating_10">` → 클래스명에서 10점 만점 숫자 추출
- **내용:** `<div class="revwCont">` 내부 텍스트
- **제목:** `<div class="topTit">` 내부 텍스트

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

> 일일 작업 로그는 `docs/daily/2026-05-12.md` 파일을 참조하세요.

### 다음 세션에서 이어갈 작업 (우선순위 순):

1.  **🔴 `scraper.py` 코드 정리** (5분)
    *   디버깅용 `print(soup)`, `print(a_tag)` 제거.
    *   주석 처리된 헤더 관련 코드 정리.
2.  **🔴 `fetch_yes24_review(goods_id)` 구현** (핵심 작업)
    *   모바일 엔드포인트 호출 + BeautifulSoup 파싱.
    *   위 섹션 3의 "구현을 위한 분석 완료 사항" 참조.
    *   교보 함수(`fetch_kyobo_book_reviews`)와 동일한 반환 형식 유지: `[{"content": ..., "rating": ..., "source_review_id": ..., "source_site": "yes24"}]`
3.  **🔴 `get_yes24_reviews(isbn)` 완성** (1분)
    *   `fetch_yes24_goods_id` → `fetch_yes24_review` 연결.
4.  **🟡 알라딘(Aladin) 리뷰 수집 채널 확장**
5.  **🟡 "나의 도서관" 프론트엔드 UI 구현**
6.  **🟢 AI 요약 기능 연동 (Step 5)**

## 6. 다음 AI를 위한 행동 지침 (Instruction for Next AI)

1.  이 파일(`continuation_context.md`)을 읽은 후 사용자에게 정중히 인사하며, **Yes24 상품 ID 추출 성공과 봇 감지 해결을 축하**하는 코멘트로 시작할 것.
2.  **[필수]** 본격적인 코딩 시작 전, 오늘 배운 내용을 기반으로 **5문제짜리 워밍업 퀴즈를 출제**할 것. 범위: BeautifulSoup 클래스 필터링, HTTP 헤더 역할, `requests` 기본 동작, CSS 클래스 기반 데이터 추출, 크롤링 윤리(robots.txt). 결과는 `docs/QUIZ_LOG.md`에 기록.
3.  첫 번째 작업은 **`scraper.py` 디버깅 코드 정리 → `fetch_yes24_review` 구현**이다.
4.  코드를 보여주지 말고 **방향과 논리만 안내**할 것.
5.  사용자가 개념에 대해 깊이 있는 질문을 할 때, 비유를 활용하여 '왜 이렇게 해야 하는지'를 함께 전달할 것. 심화 토론 내용은 `docs/QNA_ARCHIVE.md`에 기록.
6.  **[자동화 지침]** 세션 종료 시 이 파일을 업데이트하고, 즉시 커밋/푸시할 것.
