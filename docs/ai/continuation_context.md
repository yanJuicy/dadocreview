# 🤖 AI 세션 인수인계 문서 (Dodori Project Context)

> **생성일시:** 2026-04-23
> **목적:** AI 세션 변경 시 백컨텍스트 유지 및 원활한 작업 재개
> **저장소 위치:** `docs/ai/continuation_context.md` (새로운 AI 세션이 시작되면 가장 먼저 읽어볼 것)

---

## 1. 프로젝트 및 사용자 요약 (Project & User Persona)

*   **프로젝트명:** 도도리 (Dodori) - 도서관 도서 리뷰
*   **성격:** 여러 서점의 책 리뷰를 수집/분석하고 주변 도서관 소장 여부를 알려주는 FastAPI 기반 웹 서비스.
*   **사용자 성향:** 
    *   복잡한 설정보다 "가장 쉽고 심플한 방법"을 선호함.
    *   직접 코드를 타이핑하며 체득하는 '사용자 주도 코딩' 방식을 원함 (AI는 가이드를 주고 코드를 통째로 작성해주기보다는 방향을 제시해야 함).
    *   무료 인프라(PaaS, DB 등)를 적극 활용하여 포트폴리오를 유지하고자 함.

## 2. 현재 달성 상태 (Current Progress)

*   **Step 1 & 2 완료:** FastAPI 기틀 마련, DB 모델링 완료 (SQLite), 정보나루 API 기반 검색/저장 E2E 완성.
*   **Step 3 완료 (리뷰 크롤링):** 교보문고 하이브리드(HTML+API) 스크래퍼 완성, 상세 페이지(`/books/{id}`) 비동기 통신을 통한 리뷰 저장 로직 적용.
*   **배포 성공 (2026-04-23):** 
    *   `requirements.txt`에 `requests`, `beautifulsoup4`, `uvicorn[standard]` 반영 완료.
    *   **Render.com (Web Service Free Tier)** 배포 성공.
    *   **Live URL:** `https://dadocreview.onrender.com/`

## 3. 주요 기술적 의사결정 (Key Technical Decisions)

*   **PaaS:** AWS EC2가 아닌 **Render.com** 선택 (무기한 무료 유지 목적).
*   **Database:** 배포 환경에서 데이터가 휘발성(초기화)을 가지는 것을 인지하고 있으나, 설정의 간편함을 위해 현재는 **SQLite(`sql_app.db`)**를 그대로 유지. 
    *   *향후 데이터 영속성이 꼭 필요해질 때 Supabase 또는 Turso로 마이그레이션할 계획.*
*   **CI/CD:** Render의 기본 자동 배포(Auto-Deploy) 기능으로 일차 배포는 성공했으나, 향후 품질 검증을 위해 **GitHub Actions** 기반 워크플로우를 도입할 옵션을 열어둠.

## 4. 다음 세션(Next Session) 시작 위치 및 선택지

사용자는 Render 배포 성공 직후 휴식을 취하러 갔습니다. 다음 세션이 시작되면, 사용자가 아래 **두 가지 트랙** 중 어떤 것을 먼저 진행할지 물어보고 이어나가세요.

> 상세 내용은 `docs/daily/2026-04-23.md` 파일에 기록되어 있습니다. 진행 시 반드시 해당 문서를 참조하세요.

### 🔴 옵션 A: 인프라 고도화 트랙 (CI/CD)
*   **목표:** GitHub Actions 기반 파이프라인 구축.
*   **작업 내용:** Render Auto-Deploy 끄기 -> Deploy Hook 발행 -> `.github/workflows/ci-cd.yml` 작성 -> push 조건 배포.

### 🟡 옵션 B: 기능 및 UX 고도화 트랙 (프로젝트 기능 채우기)
*   **목표:** 서비스 완성도 향상.
*   **작업 내용 (우선순위 순):**
    1.  **검색 결과 페이징 적용:** `naru_api.py` 수정(`pageNo`, `pageSize` 파라미터 활용), UI 페이징 추가.
    2.  **상세 페이지 보강:** 외부 서점 링크, ISBN, 책 설명 데이터 연동.
    3.  **UI/UX 디자인 개선:** CSS 변수 체계 도입, 반응형 및 카드 호버 애니메이션 추가 등.
    4.  **리뷰 스크래퍼 확장:** Yes24, 알라딘 리뷰 시스템 분석 스크래핑 추가.

## 5. 다음 AI를 위한 행동 지침 (Instruction for Next AI)

1.  이 파일(`continuation_context.md`)을 읽은 후 사용자에게 정중히 인사하며, 지난번 **Render 배포 성공을 축하**하는 코멘트로 시작할 것.
2.  사용자에게 **[옵션 A. GitHub Actions CI/CD 적용]**과 **[옵션 B. 정보나루 API 등 코드 기능 고도화]** 중 오늘 어떤 것부터 시작할지 물어볼 것.
3.  구체적인 기술 가이드가 필요할 경우 반드시 `docs/daily/2026-04-23.md` 파일과 프로젝트의 기존 패턴(`crud.py`, `scraper.py`)을 우선 참조할 것.
