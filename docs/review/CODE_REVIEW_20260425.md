# 🔍 도도리 프로젝트 — 종합 코드 리뷰 & 보완 가이드

> **분석 대상:** 전체 소스코드 + `docs/` 문서 일체  
> **분석 기준:** 기능 완성도, 코드 품질, 예외 처리, 실무 적용 가능성

---

## 📊 요약 — 보완 필요 항목 총정리

| 카테고리 | 심각도 | 항목 수 |
| :--- | :---: | :---: |
| 🔴 **예외 처리 / 장애 대응** | 높음 | 7개 |
| 🟡 **기능 미완성 / 누락** | 중간 | 6개 |
| 🟢 **코드 품질 / 실무 관례** | 낮음 | 6개 |

---

## 🔴 1. 예외 처리 / 장애 대응 (실무에서 가장 중요)

### 1-1. `naru_api.py` — 외부 API 호출에 예외 처리 전무

**현재 코드:** [naru_api.py:17-37](file:///home/yanju/projects/dadoc_review/app/services/naru_api.py#L17-L37)

```python
def fetch_books_from_naru(keyword: str):
    url = f"http://data4library.kr/api/srchBooks?authKey={NARU_API_KEY}&format=json&title={keyword}"
    response = requests.get(url)       # ← 타임아웃 없음
    data = response.json()             # ← 응답이 JSON이 아닐 때 크래시
```

**문제점:**
- `requests.get()`에 **timeout이 없어서** 정보나루 서버가 응답하지 않으면 **앱 전체가 영구 대기**
- 네트워크 에러(DNS 실패, 연결 거부 등) 시 **500 서버 에러**가 사용자에게 그대로 노출
- API 키가 잘못되었거나 만료 시 **응답이 JSON이 아닐 수 있음** → `.json()` 크래시
- HTTP 상태 코드(4xx, 5xx) 검증 없음

**보완 방향:**
```python
# 실무에서의 외부 API 호출 패턴
try:
    response = requests.get(url, timeout=5)    # 타임아웃 필수
    response.raise_for_status()                 # 4xx/5xx 검증
    data = response.json()
except requests.exceptions.Timeout:
    # 타임아웃 처리
except requests.exceptions.RequestException:
    # 네트워크 에러 처리
except ValueError:
    # JSON 파싱 실패 처리
```

---

### 1-2. `scraper.py` — 스크래핑 함수 전체에 예외 처리 없음

**현재 코드:** [scraper.py:58-61](file:///home/yanju/projects/dadoc_review/app/services/scraper.py#L58-L61)

```python
def get_kyobo_reviews(isbn):
    book_id = get_kyobo_book_id(isbn)     # ← None 반환 가능
    reviews = fetch_kyobo_book_reviews(book_id)  # ← None이 들어오면 크래시
    return reviews
```

**문제점:**
- `get_kyobo_book_id()`가 `None`을 반환할 수 있는데(검색결과 없을 때), 그걸 그대로 `fetch_kyobo_book_reviews(None)`에 전달 → 크래시
- 교보문고 서버 장애나 구조 변경 시 **앱 전체가 500 에러**
- `requests.get()` 호출에도 timeout 없음
- HTML 파싱 실패 시 예외 없음

**보완 방향:**
```python
def get_kyobo_reviews(isbn):
    book_id = get_kyobo_book_id(isbn)
    if not book_id:
        return []  # 빈 리스트 반환 (graceful degradation)
    
    try:
        reviews = fetch_kyobo_book_reviews(book_id)
        return reviews
    except Exception as e:
        print(f"교보문고 리뷰 수집 실패: {e}")
        return []
```

---

### 1-3. `main.py` — 라우터에서 예외 전파 차단 없음

**현재 코드:** [main.py:45-56](file:///home/yanju/projects/dadoc_review/app/main.py#L45-L56)

```python
@app.get("/results", response_class=HTMLResponse)
def read_results(request: Request, q: str = None, db: Session = Depends(get_db)):
    external_books = naru_api.fetch_books_from_naru(q)  # ← 여기서 크래시하면?
    crud.sync_books(db, external_books)                  # ← 전부 날아감
```

**문제점:**
- `q`가 `None`이거나 빈 문자열일 때의 검증 없음 → API에 `None` 키워드로 호출됨
- 외부 API 장애 시 사용자에게 **빈 화면도 아닌 에러 페이지**가 뜸
- 리뷰 라우터(`/books/{book_id}/reviews`)도 마찬가지

**보완 방향:**
```python
@app.get("/results", response_class=HTMLResponse)
def read_results(request: Request, q: str = None, db: Session = Depends(get_db)):
    if not q or not q.strip():
        return templates.TemplateResponse(request, "results.html", {"keyword": q, "books": []})

    try:
        external_books = naru_api.fetch_books_from_naru(q)
        crud.sync_books(db, external_books)
    except Exception:
        pass  # 외부 API 실패해도 DB에서라도 검색

    books = crud.search_books_by_title(db=db, title=q)
    # ...
```

---

### 1-4. `main.py` — 존재하지 않는 book_id 접근 시 처리 없음

**현재 코드:** [main.py:64-67](file:///home/yanju/projects/dadoc_review/app/main.py#L64-L67)

```python
@app.get("/books/{book_id}")
def read_book(book_id: int, request: Request, db: Session = Depends(get_db)):
    book = crud.read_book_by_id(db, book_id)  # ← None 가능
    return templates.TemplateResponse(request, "book_detail.html", {"book": book})
    # ← book이 None이면 템플릿에서 book.title 접근 시 500 에러
```

**보완 방향:**
```python
from fastapi import HTTPException

book = crud.read_book_by_id(db, book_id)
if not book:
    raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다")
```

---

### 1-5. `crud.py` — sync_books에서 commit 실패 시 롤백 없음

**현재 코드:** [crud.py:46-54](file:///home/yanju/projects/dadoc_review/app/crud.py#L46-L54)

```python
def sync_books(db: Session, books_data: list):
    for book in books_data:
        isbn = book.get("isbn")
        # ...
        if not existing_book:
            create_book(db, book)  # ← 내부에서 개별 commit 발생
```

**문제점:**
- `create_book()` 안에서 **개별 commit**을 하고 있어서, 10권 중 5번째 책에서 에러나면 4권은 저장되고 나머지는 안 됨 (부분 실패)
- DB 에러 시 session이 dirty 상태로 남을 수 있음
- `isbn`이 `None`이거나 빈 문자열인 경우 검증 없음

**보완 방향:**
```python
def sync_books(db: Session, books_data: list):
    for book in books_data:
        isbn = book.get("isbn")
        if not isbn:           # ← ISBN 없는 데이터 스킵
            continue
        # ...
    # 한 번에 commit (원자성 보장)
```

---

### 1-6. `book_detail.js` — 변수 선언 키워드 누락 + 에러 처리 없음

**현재 코드:** [book_detail.js:1-27](file:///home/yanju/projects/dadoc_review/app/static/js/book_detail.js#L1-L27)

```javascript
$reviewFetchForm = document.getElementById("review-fetch-form");  // ← const/let 없음 → 전역 변수
$reviewList = document.getElementById("review-list");              // ← 동일

// ...
bookId = $reviewFetchForm.dataset.bookId;    // ← 전역 변수
response = await fetch("/books/" + bookId + "/reviews");  // ← 전역 변수
reviews = await response.json();             // ← 에러 처리 없음
```

**문제점:**
- `const`/`let` 없이 변수를 선언 → **모두 전역 변수(window 객체)로 등록됨** (실무에서 지적받는 대표적 안티패턴)
- `$reviewFetchForm`가 `null`일 수 있음 (리뷰가 이미 있는 상태에서 접근 시) → 에러
- fetch 실패(네트워크 에러, 서버 에러) 시 처리 없음
- 사용자에게 로딩 상태(스피너) 미표시

**보완 방향:**
```javascript
const $reviewFetchForm = document.getElementById("review-fetch-form");
const $reviewList = document.getElementById("review-list");

if ($reviewFetchForm) {  // null 체크
    $reviewFetchForm.addEventListener("submit", async function(e) {
        e.preventDefault();
        try {
            const response = await fetch(/* ... */);
            if (!response.ok) throw new Error("서버 에러");
            const reviews = await response.json();
            // ...
        } catch (error) {
            // 사용자에게 에러 메시지 표시
        }
    });
}
```

---

### 1-7. `main.js` — 검색어 인코딩 처리 없음

**현재 코드:** [main.js:4-8](file:///home/yanju/projects/dadoc_review/app/static/js/main.js#L4-L8)

```javascript
$searchBtn.addEventListener('click', () => {
    const keyword = $searchInput.value;
    if (keyword) {
        window.location.href = `/results?q=${keyword}`;  // ← URL 인코딩 없음
    }
});
```

**문제점:**
- 특수문자(`&`, `#`, `=`, 공백 등) 포함된 검색어가 URL을 깨트릴 수 있음
- 빈 공백만 입력해도 통과됨 (`"   "` → truthy)

**보완 방향:**
```javascript
const keyword = $searchInput.value.trim();
if (keyword) {
    window.location.href = `/results?q=${encodeURIComponent(keyword)}`;
}
```

---

## 🟡 2. 기능 미완성 / 누락

### 2-1. 검색 결과 페이징 미구현

**현황:** `naru_api.py`가 **첫 페이지 10건만 반환**. `pageNo`, `pageSize` 파라미터 미사용.

**영향 범위:**
- [naru_api.py](file:///home/yanju/projects/dadoc_review/app/services/naru_api.py) — 파라미터 추가
- [main.py](file:///home/yanju/projects/dadoc_review/app/main.py) — `page` 쿼리 파라미터 처리
- [results.html](file:///home/yanju/projects/dadoc_review/app/templates/results.html) — 페이지네이션 UI
- [style.css](file:///home/yanju/projects/dadoc_review/app/static/css/style.css) — 페이지네이션 스타일

> 상세 구현 가이드: [docs/daily/2026-04-23.md 섹션 3](file:///home/yanju/projects/dadoc_review/docs/daily/2026-04-23.md#L267)

---

### 2-2. 상세 페이지 정보 부족

**현재 표시 항목:** 표지, 제목, 저자 (3개뿐)

**누락 항목 (DB 모델에는 이미 있지만 사용 안 됨):**

| 필드 | `models.py` 정의 | `naru_api.py`에서 수집 | `book_detail.html` 표시 |
| :--- | :---: | :---: | :---: |
| ISBN | ✅ | ✅ | ❌ |
| 책 설명 (description) | ✅ | ❌ | ❌ |
| 평균 별점 | ✅ | ❌ | ❌ |
| 리뷰 수 | ✅ | ❌ | ❌ |
| 교보문고 링크 | ✅ | ❌ | ❌ |
| Yes24 링크 | ✅ | ❌ | ❌ |
| 알라딘 링크 | ✅ | ❌ | ❌ |

---

### 2-3. `sync_books`에서 기존 데이터 업데이트(Update) 미구현

**현재 코드:** [crud.py:46-54](file:///home/yanju/projects/dadoc_review/app/crud.py#L46-L54)

```python
def sync_books(db: Session, books_data: list):
    for book in books_data:
        isbn = book.get("isbn")
        existing_book = db.execute(stmt).scalar_one_or_none()
        if not existing_book:
            create_book(db, book)    # ← INSERT만 있고 UPDATE가 없음
```

**문제:** 한 번 DB에 저장된 책의 정보(표지 URL, 제목 등)가 정보나루에서 변경되어도 **영원히 업데이트되지 않음**. 이것은 "Upsert" 패턴이어야 하는데 현재 "Insert only" 상태.

---

### 2-4. 리뷰 가져오기 버튼 — "이미 있으면 숨김" 로직의 한계

**현재 코드:** [book_detail.html:28-34](file:///home/yanju/projects/dadoc_review/app/templates/book_detail.html#L28-L34)

```html
{% if not book.reviews %}
<form id="review-fetch-form" data-book-id="{{book.id}}">
    <button type="submit" class="fetch-review-btn">리뷰 가져오기 💬</button>
</form>
{% endif %}
```

**문제:** 리뷰가 한 번이라도 저장되면 버튼이 **영구히 사라짐**. 새 리뷰가 추가되었을 수 있는데 갱신할 방법이 없음. "리뷰 새로고침" 기능이 필요.

---

### 2-5. results.html — 검색 결과 페이지에 검색창 없음

검색 결과를 보다가 **다른 키워드로 재검색**하려면 메인으로 돌아가야 함. `results.html`에 검색창이 없음.

---

### 2-6. 에러/로딩 UI 부재

| 상황 | 현재 처리 | 실무 기준 |
| :--- | :--- | :--- |
| 리뷰 가져오기 중 | 아무 피드백 없음 | 로딩 스피너/텍스트 표시 |
| API 에러 발생 | 500 에러 페이지 | 사용자 친화적 에러 메시지 |
| 검색 결과 0건 | 짧은 텍스트만 | 재검색 유도 UI |
| 404 페이지 | FastAPI 기본 JSON | 커스텀 404 페이지 |

---

## 🟢 3. 코드 품질 / 실무 관례

### 3-1. `database.py` — deprecated API 사용

**현재:** [database.py:10](file:///home/yanju/projects/dadoc_review/app/database.py#L10)
```python
from sqlalchemy.ext.declarative import declarative_base  # ← deprecated since SQLAlchemy 2.0
```

**실무 기준:**
```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

---

### 3-2. `models.py` — 중복 import

**현재:** [models.py:9-10](file:///home/yanju/projects/dadoc_review/app/models.py#L9-L10)
```python
from sqlalchemy import ForeignKey                                         # ← 중복
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Table  # ← 여기에도 ForeignKey
```

---

### 3-3. `schemas.py` — `Book` 스키마에 `Config` 클래스 누락

**현재:** [schemas.py:13-27](file:///home/yanju/projects/dadoc_review/app/schemas.py#L13-L27)

`Review`에는 `class Config: from_attributes = True`가 있지만, `Book`에는 없음. ORM 모델 → Pydantic 스키마 변환 시 문제 발생 가능.

또한 현재 `Book` 스키마에서 `id`, `description`, `kyobo_link`, `yes24_link`, `aladin_link`이 **필수(required)** 로 되어있어서, create 시에 문제가 될 수 있음. Create용/Response용 스키마를 분리하는 것이 실무 관례.

**실무 패턴:**
```python
class BookBase(BaseModel):      # 공통 필드
class BookCreate(BookBase):     # 생성 시 필요한 필드
class BookResponse(BookBase):   # 응답 시 반환할 필드
    class Config:
        from_attributes = True
```

---

### 3-4. `naru_api.py` — 오탈자

**현재:** [naru_api.py:28](file:///home/yanju/projects/dadoc_review/app/services/naru_api.py#L28)
```python
refiend_book = {    # ← "refined"의 오탈자
```

---

### 3-5. HTML 템플릿 — 인라인 스타일 사용

**현재:** `results.html`, `book_detail.html`에서 `style="text-decoration: none; color:inherit;"` 같은 인라인 스타일을 사용 중.

```html
<!-- results.html:26 -->
<a href="/books/{{book.id}}" style="text-decoration: none; color:inherit;">
```

CSS 클래스로 분리하는 것이 유지보수·일관성 측면에서 좋음.

---

### 3-6. 공통 레이아웃(base template) 없음

현재 `index.html`, `results.html`, `book_detail.html` 3개 파일에서 **`<head>`, `<header>` 영역이 거의 동일하게 복사-붙여넣기**되어 있음.

**실무 기준:** Jinja2의 `{% extends "base.html" %}` / `{% block content %}` 패턴으로 공통 레이아웃을 분리해야 함. 안 그러면 나중에 폰트 하나 바꾸려면 3개 파일 모두 수정해야 함.

---

## 📋 우선순위별 작업 추천

### 🔴 오늘 반드시 (실무 기본기)

| # | 작업 | 수정 파일 | 예상 시간 |
| :---: | :--- | :--- | :---: |
| 1 | 외부 API 호출에 timeout + try/except 추가 | `naru_api.py` | 15분 |
| 2 | 스크래퍼 None 체크 + try/except 추가 | `scraper.py` | 15분 |
| 3 | 라우터에서 q 빈 값 검증 + book 404 처리 | `main.py` | 15분 |
| 4 | JS 변수 선언 키워드 + null 체크 + encodeURI | `main.js`, `book_detail.js` | 15분 |

### 🟡 이번 주 내로 (기능 완성도)

| # | 작업 | 수정 파일 | 예상 시간 |
| :---: | :--- | :--- | :---: |
| 5 | 검색 결과 페이징 | `naru_api.py`, `main.py`, `results.html` | 1시간 |
| 6 | 상세 페이지 콘텐츠 보강 (ISBN, description) | `naru_api.py`, `crud.py`, `book_detail.html` | 1시간 |
| 7 | sync_books를 Upsert 로직으로 변경 | `crud.py` | 30분 |
| 8 | 로딩 스피너 + 에러 메시지 UI | `book_detail.js`, `style.css` | 30분 |

### 🟢 여유 있을 때 (코드 품질)

| # | 작업 | 수정 파일 | 예상 시간 |
| :---: | :--- | :--- | :---: |
| 9 | base.html 공통 레이아웃 도입 | 전체 HTML | 30분 |
| 10 | schemas.py Create/Response 분리 | `schemas.py` | 20분 |
| 11 | deprecated API 교체 | `database.py` | 5분 |
| 12 | 인라인 스타일 → CSS 클래스 분리 | HTML, CSS | 15분 |
