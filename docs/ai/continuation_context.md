# 🤖 AI 세션 인수인계 문서 (Dodori Project Context)

> **최종 갱신일시:** 2026-04-26
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
    *   개념에 대해 깊이 있는 질문을 자주 함 (예: "왜 try-except인데 raise를 또 해?", "예측 가능한 에러가 뭐야?"). **비유와 단계별 설명으로 정확하게 답해야 함.**

## 2. 현재 달성 상태 (Current Progress)

*   **Step 1 & 2 완료:** FastAPI 기틀 마련, DB 모델링 완료 (SQLite), 정보나루 API 기반 검색/저장 E2E 완성.
*   **Step 3 완료 (리뷰 크롤링):** 교보문고 하이브리드(HTML+API) 스크래퍼 완성, 상세 페이지(`/books/{id}`) 비동기 통신을 통한 리뷰 저장 로직 적용.
*   **배포 성공 (2026-04-23):** 
    *   **Render.com (Web Service Free Tier)** 배포 성공.
    *   **Live URL:** `https://dadocreview.onrender.com/`
*   **Step 4 진행 중 (2026-04-26~):**
    *   ✅ **백엔드 예외 처리 강화 완료:**
        *   `naru_api.py`: 외부 API 호출 타임아웃(5s) + `try-except` (HTTPError, Timeout)
        *   `scraper.py`: `get_kyobo_book_id` None 체크(Guard Clause) + 각 함수 타임아웃 + `try-except`
        *   `main.py`: 빈 검색어(`q.strip()`) 유효성 검사, 도서 상세/리뷰 라우터에 404 `HTTPException` 처리
    *   ❌ **프론트엔드 안정화 미착수:** `main.js`(`encodeURIComponent`), `book_detail.js`(`const`/`let`, `try-catch`)
    *   ❌ **검색 결과 페이지네이션 미착수**
    *   ❌ **상세 페이지 콘텐츠 보강 미착수**

## 3. 주요 기술적 의사결정 (Key Technical Decisions)

*   **PaaS:** AWS EC2가 아닌 **Render.com** 선택 (무기한 무료 유지 목적).
*   **Database:** 배포 환경에서 데이터가 휘발성(초기화)을 가지는 것을 인지하고 있으나, 설정의 간편함을 위해 현재는 **SQLite(`sql_app.db`)**를 그대로 유지. 
    *   *향후 데이터 영속성이 꼭 필요해질 때 Supabase 또는 Turso로 마이그레이션할 계획.*
*   **CI/CD:** Render의 기본 자동 배포(Auto-Deploy) 기능으로 일차 배포는 성공했으나, 향후 품질 검증을 위해 **GitHub Actions** 기반 워크플로우를 도입할 옵션을 열어둠.
*   **예외 처리 레이어링 (2026-04-26 확립):**
    *   서비스 레이어(`services/`): `try-except`로 외부 장애 흡수 → 빈 리스트 반환 (Graceful Degradation)
    *   라우터 레이어(`main.py`): `if` + `raise HTTPException`으로 비즈니스 규칙 위반 처리 (Guard Clause)
    *   이유: 서비스 레이어는 HTTP에 의존하지 않아야 다른 환경에서 재사용 가능

## 4. 다음 세션(Next Session) 시작 위치

사용자는 백엔드 예외 처리를 완료한 후 휴식을 취하러 갔습니다.

> 상세 코드 리뷰 및 보완 항목 전체 목록은 `docs/review/CODE_REVIEW_20260425.md` 파일을 참조하세요.
> 일일 작업 로그는 `docs/daily/2026-04-26.md` 파일을 참조하세요.

### 다음 세션에서 이어갈 작업 (우선순위 순):

1.  **🔴 프론트엔드 안정화 (JS)** — 약 15분
    *   `main.js`: `$searchInput.value.trim()` + `encodeURIComponent(keyword)` 적용
    *   `book_detail.js`: 모든 변수에 `const`/`let` 추가, `$reviewFetchForm` null 체크, `fetch` 호출 `try-catch` 감싸기
2.  **🟡 검색 결과 페이지네이션** — 약 1시간
    *   `naru_api.py`에 `pageNo`, `pageSize` 파라미터 추가
    *   `main.py` 라우터에 `page` 쿼리 파라미터 처리
    *   `results.html`에 이전/다음 페이지 UI 추가
3.  **🟡 상세 페이지 콘텐츠 보강** — 약 1시간
    *   `naru_api.py`에서 `description` 등 추가 필드 수집
    *   `book_detail.html`에 ISBN, 설명, 서점 링크 표시

## 5. 다음 AI를 위한 행동 지침 (Instruction for Next AI)

1.  이 파일(`continuation_context.md`)을 읽은 후 사용자에게 정중히 인사하며, **백엔드 예외 처리 완료를 축하**하는 코멘트로 시작할 것.
2.  **[새로운 지침]** 그 날의 본격적인 코딩 작업을 시작하기 전에 가벼운 워밍업으로 **5문제짜리 퀴즈를 출제할 것**.
    *   범위: Python 기초, FastAPI 관련 개념, 이 프로젝트에서 작성한 이전 코드, 학습한 중요 개념.
    *   퀴즈를 내어 사용자가 생각을 환기할 수 있게 돕고, 정답과 피드백을 제공한다.
    *   퀴즈 출제 내용과 결과는 `docs/QUIZ_LOG.md` 파일에 기록하여 지속적으로 관리한다.
3.  퀴즈가 끝난 뒤에는 **프론트엔드 안정화(JS) 가이드**부터 시작할 것. 코드를 보여주지 말고 **방향과 논리만 안내**할 것.
4.  사용자가 개념에 대해 깊이 있는 질문을 할 때, 비유를 활용하여 본질을 설명해 줄 것. 단순히 "이렇게 하세요"가 아니라 **"왜 이렇게 해야 하는지"**를 항상 함께 전달할 것. **분리된 `docs/QNA_ARCHIVE.md` 에 기록하여 관리할 것.**
5.  구체적인 기술 가이드가 필요할 경우 `docs/review/CODE_REVIEW_20260425.md` 와 `docs/daily/2026-04-23.md` 파일 등을 우선 참조할 것.
