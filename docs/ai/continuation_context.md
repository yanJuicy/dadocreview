# 🤖 AI 세션 인수인계 문서 (Dodori Project Context)

> **최종 갱신일시:** 2026-04-30
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
    *   ✅ **도서관 연동 UML 설계 완료** (`docs/UML_05_LIBRARY_INTEGRATION.md`):
        *   `localStorage` 기반 "나의 도서관" 설정 시나리오
        *   검색 결과 페이지 비동기(fetch) 대출 가능 여부 조회 시나리오
        *   상세 페이지 `Geolocation` API 기반 주변 도서관 조회 시나리오
    *   ✅ **`Library` DB 모델 설계** (`app/models.py`): `lib_code`, `name`, `address`, `phone`, `latitude`, `longitude`, `homepage`, `closed_days_info` 컬럼 포함.
    *   ✅ **전국 도서관 DB 마이그레이션 완료** (`scripts/import_libraries.py`):
        *   정보나루 참여 도서관 목록 엑셀 파일 (`data/libraries.xlsx`) → SQLite 이관.
        *   **1,594개 도서관** 데이터 저장 완료.
        *   `pandas` + `openpyxl` 활용. `header=7` 옵션으로 헤더 파싱 이슈 해결.
    *   ✅ **도서관 검색 API 구축** (`app/crud.py`, `app/main.py`):
        *   `search_libraries(db, library_name)` 함수: `Library.name.contains()` 활용한 LIKE 검색.
        *   `GET /api/libraries?q=검색어` 엔드포인트: 빈 검색어 방어 로직 포함.

## 3. 주요 기술적 의사결정 (Key Technical Decisions)

*   **도서관 데이터 전략: 로컬 DB 선택 (2026-04-30 확립)**
    *   정보나루 `libSrch` API는 이름 검색을 지원하지 않기 때문에, 전국 참여 도서관 목록 엑셀 파일을 최초 1회 파싱하여 SQLite에 저장(Seeding)하는 전략 채택.
    *   **장점:** 외부 API 의존도 Zero → 검색 속도 극대화, 안정성 향상, 명 검색 자유.
*   **PaaS:** Render.com (무기한 무료 유지).
*   **Database:** SQLite (`sql_app.db`). Render에서 DB가 휘발성(배포 시 초기화)을 가짐을 인지. `import_libraries.py`를 Start Command에 연결하여 자동 재시딩하는 방식으로 대응 예정.
*   **AI 리뷰 기능:** Gemini API가 아닌 **Hugging Face `transformers` 라이브러리 + 오픈소스 한국어 요약 모델(예: KoBART) 직접 구동** 방식으로 구현할 예정.

## 4. 다음 세션(Next Session) 시작 위치

> 일일 작업 로그는 `docs/daily/2026-04-30.md` 파일을 참조하세요.

### 다음 세션에서 이어갈 작업 (우선순위 순):

1.  **🔴 "나의 도서관" 프론트엔드 UI 구현** (가장 먼저!)
    *   `index.html`(메인 화면)에 도서관 검색창 및 결과 목록 UI 추가.
    *   사용자가 도서관을 선택하면 `localStorage`에 저장(`myLibraries: [{libCode, name}]`)하는 `main.js` 로직 구현.
    *   선택된 "나의 도서관" 목록을 화면에 표시하고 삭제하는 기능 구현.
2.  **🟡 검색 결과 페이지 — 대출 가능 여부 비동기 조회**
    *   검색 결과(`results.html`) 렌더링 후, `localStorage`의 도서관 코드와 각 책의 ISBN을 백엔드로 보내 대출 가능 여부를 비동기로 조회하는 `fetch` 로직 추가 (`results.js`).
    *   백엔드(`main.py`, `naru_api.py`)에 정보나루 `bookExist` API 연동 함수 추가.
3.  **🟢 Render 배포 시 도서관 DB 자동 시딩 설정**
    *   Render 대시보드의 `Start Command`를 `python -m scripts.import_libraries && uvicorn ...`으로 변경.

## 5. 다음 AI를 위한 행동 지침 (Instruction for Next AI)

1.  이 파일(`continuation_context.md`)을 읽은 후 사용자에게 정중히 인사하며, **도서관 DB 구축 완료를 축하**하는 코멘트로 시작할 것.
2.  **[필수]** 본격적인 코딩 시작 전, 오늘 배운 내용을 기반으로 **5문제짜리 워밍업 퀴즈를 출제**할 것. 범위: `pandas` 헤더 파싱, SQLAlchemy LIKE 검색, `localStorage` 개념, FastAPI 라우터 등. 결과는 `docs/QUIZ_LOG.md`에 기록.
3.  첫 번째 작업은 **"나의 도서관" 메인 화면 UI 구현 (프론트엔드)**이다. `GET /api/libraries?q=...` 엔드포인트가 이미 준비되어 있으므로, 이를 `fetch`로 호출하는 `main.js` 로직과 UI 작성을 가이드할 것.
4.  코드를 보여주지 말고 **방향과 논리만 안내**할 것.
5.  사용자가 개념에 대해 깊이 있는 질문을 할 때, 비유를 활용하여 '왜 이렇게 해야 하는지'를 함께 전달할 것. 심화 토론 내용은 `docs/QNA_ARCHIVE.md`에 기록.
6.  **[자동화 지침]** 세션 종료 시 이 파일을 업데이트하고, 즉시 커밋/푸시할 것.

