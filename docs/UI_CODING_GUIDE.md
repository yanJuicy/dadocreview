# 🎨 도도리 UI 직접 코딩 가이드

> **목표**: `docs/imgs`의 디자인 목업을 보고, `app/templates`의 HTML과 `app/static/css`의 CSS 파일을 직접 작성해 완성하기
> **디자인 기준**: 모바일 우선(Mobile First) 레이아웃

---

## 📁 1. 현재 파일 구조

```
app/
├── templates/
│   ├── index.html         ← 메인 홈 페이지 (작업 중)
│   ├── results.html       ← 검색 결과 페이지 (미작업)
│   └── book_detail.html   ← 책 상세 페이지 (미작업)
│
└── static/
    ├── css/
    │   ├── common.css     ← 모든 페이지 공통 스타일 (작업 중)
    │   ├── index.css      ← 메인 페이지 전용 스타일 (작업 중)
    │   ├── results.css    ← 검색 결과 페이지 전용 (미작업)
    │   ├── book_detail.css← 상세 페이지 전용 (미작업)
    │   └── style.css      ← (미사용, 무시)
    │
    ├── images/
    │   └── logo.png       ← 도도리 로고 이미지 ✅ 존재함
    │
    └── js/
        ├── main.js        ← 메인 페이지 동작
        └── book_detail.js ← 상세 페이지 동작
```

> [!IMPORTANT]
> **HTML 작업 → `app/templates/`** | **스타일 작업 → `app/static/css/`**
> 정적 파일(이미지, CSS, JS)은 HTML에서 반드시 Jinja2의 `url_for` 문법으로 불러온다.
> 예: `href="{{ url_for('static', path='/css/common.css') }}"`

---

## 🎨 2. 디자인 시스템 (현재 적용 중인 값들)

### 색상 팔레트

```css
/* 배경 */
background: white;               /* body 전체 배경 */
background-color: #f5f5f7;       /* 섹션 구분선, 태그 배경, 검색창 배경 */

/* 텍스트 */
color: #333333;                  /* 기본 텍스트 (로고 등) */
color: #888888;                  /* 보조 텍스트 (서브타이틀, 전체삭제 버튼 등) */
color: rgb(45, 45, 45);          /* 태그 글씨 */

/* 테두리 */
border: 1px solid rgba(0,0,0,0.06);  /* 태그 테두리 */
border-bottom: 2px solid #f5f5f7;    /* 헤더 구분선 */

/* 목업에서 아직 미적용된 색상 (앞으로 사용 예정) */
/* --blue-primary: #5B8DEF;   주요 버튼 */
/* --green-available: #4ECDC4; 대출 가능 뱃지 */
/* --star-yellow: #FFB800;    별점 */
```

### 폰트
- **영문/숫자**: `Inter` (Google Fonts)
- **한글**: `Noto Sans KR` (Google Fonts)
- `index.html` `<head>`에 Google Fonts 링크로 로드 중

### 레이아웃 원칙
- **PC 브라우저 전체 너비** 사용 (모바일 제한 없음)
- 각 섹션 내부에서 좌우 `padding`으로 여백 조절
- 섹션 간 구분은 `border-top: 10px solid #f5f5f7` 방식 사용

---

## 📋 3. 작업 체크리스트

### ✅ 완료된 작업

#### `common.css`
- [x] `html, body` 초기화 (`margin: 0`, `padding: 0`, `background-color: white`)
- [x] 폰트 설정 (`font-family: 'Inter', 'Noto Sans KR', sans-serif`)
- [x] `.app-container` 전체 레이아웃 컨테이너 (`width: 100%`, flex column)
- [x] `header` 스타일 (중앙 정렬, 하단 구분선 `border-bottom: 2px solid #f5f5f7`)
- [x] `.logo` 스타일 (inline-flex, 링크 밑줄 제거, 이미지+텍스트 가로 정렬)
- [x] `.logo img` 크기 (`width: 60px`)
- [x] `.logo-subtitle` 보조 텍스트 스타일
- [x] `.search-section` 여백 (`padding: 24px 20px`)
- [x] `.search-box` 검색창 컨테이너 (flex, 배경색 `#f5f5f7`, `border-radius: 16px`)
- [x] `#searchInput` 스타일 (투명 배경, 테두리 없음, flex-grow: 1)
- [x] `#searchBtn` 스타일 (투명 배경, 테두리 없음, cursor: pointer)

#### `index.css`
- [x] `.recent-search` 섹션 (상단 구분선 `border-top: 10px solid #f5f5f7`)
- [x] `.recent-header` 타이틀+삭제버튼 가로 배치 (`justify-content: space-between`)
- [x] `.recent-header h3` 폰트 스타일
- [x] `.clear-all-btn` 버튼 스타일
- [x] `.recent-tags` 태그 목록 컨테이너 (flex, gap: 8px)
- [x] `.recent-tag-item` 태그 칩 스타일 (배경, border-radius: 20px, padding)
- [x] `.recent-tags-empty` 빈 상태 안내 텍스트
- [x] `.favorites` 즐겨찾기 섹션 (flex column, flex-grow: 1로 남은 화면 채우기, padding-bottom: 80px)
- [x] `.favorites h3` 타이틀 스타일
- [x] `.favorites-books` 가로 스크롤 컨테이너 (flex, overflow-x: auto, flex-grow: 1)
- [x] `.favorite-card` 카드 스타일 (flex column, 고정 width/height, flex-shrink: 0)
- [x] `.favorite-card img` 표지 이미지 (border-radius: 8px)
- [x] `.favorite-title`, `.favorite-author` 텍스트 스타일

#### `index.html`
- [x] HTML5 기본 구조 (`<!DOCTYPE html>`, `<head>`, `<body>`)
- [x] Google Fonts 연결
- [x] `common.css`, `index.css` 연결
- [x] `.app-container` > `<header>` > `<main>` > `<nav>` 기본 뼈대
- [x] `<header>`: 로고 이미지 + "도도리" 텍스트 + 서브타이틀
- [x] `.search-section`: 검색창 (`#searchBtn` 왼쪽, `#searchInput` 오른쪽)
- [x] `.recent-search`: 최근 검색 헤더 + 태그 목록 + 빈 상태 메시지 뼈대
- [x] `<nav class="bottom-nav">`: 홈, 검색 탭바 (완성)
- [x] `.favorites`: 즐겨찾기 섹션 타이틀 + 가로 스크롤 카드 목록 + 빈 상태 메시지 분리 배치

---

### 🚧 다음에 이어서 할 작업

#### 우선순위 높음 — 현재 `index.html` 완성

1. **즐겨찾기 JavaScript 연동** ← 다음 작업
   - `main.js`: `localStorage`에서 즐겨찾기 목록 읽어서 `.favorites-books`에 카드 동적 렌더링
   - 즐겨찾기가 없으면 `.favorites-books` 숨기고 `.favorites-empty` 보이기 / 있으면 반대로
   - 현재 `index.html`의 하드코딩된 mock 카드 3개는 JS 연동 후 제거

2. **최근 검색 JavaScript 연동**
   - `main.js`: 검색어 입력 시 `localStorage`에 저장, 페이지 로드 시 `.recent-tags`에 렌더링
   - 빈 상태 시 `.recent-tags-empty` 표시 / 있으면 `.recent-tags` 표시
   - `.clear-all-btn` 클릭 시 localStorage 초기화 후 re-render

3. **추천 도서 섹션 (`<section class="recommendations">`) 추가** (현재 HTML에서 제거됨 → 재추가 필요)
   - `index.html`: 섹션 타이틀 + 책 카드 목록 뼈대 (표지, 제목, 저자, 강점/약점)
   - `index.css`: 책 카드 스타일 (대출 가능 뱃지 포함)

#### 우선순위 중간 — 다른 페이지

4. **`results.html` + `results.css` 작업**
   - 목업: `메인 페이지 - 검색.png`
   - 추가할 것: 상단 검색창 유지, 책 카드에 강점/약점 추가, 대출 가능 뱃지, 하단 탭바

5. **`book_detail.html` + `book_detail.css` 작업**
   - 목업: `상세 페이지 - 요약.png`, `상세 페이지 - 리뷰.png`, `상세 페이지 - 목차.png`, `상세 페이지 - 상세정보.png`
   - 추가할 것: 뒤로가기 버튼 헤더, 책 통계(대출/보유/평점), 도서관찾기/찜하기 버튼, 탭 메뉴(요약/상세정보/목차/리뷰)

#### 우선순위 낮음 — 새 페이지 생성

6. `library.html` — 서재 페이지 (`서재 페이지.png`)
7. `explore.html` — 탐색 페이지 (`탐색 페이지.png`)
8. `compare.html` — 비교 페이지 (`비교 페이지.png`)
9. `compare_detail.html` — 비교 폴더 상세 (`비교 페이지 - 비교 표 보기.png`)

---

## 🧩 4. 핵심 CSS 개념 정리 (학습 중 배운 것들)

### `margin: 0 auto` vs `text-align: center`
- `margin: 0 auto` → **상자(블록 요소) 자체**를 화면 가운데로 보낼 때. 단, `width`가 지정되어 있어야 함.
- `text-align: center` → **상자 안의 글자나 이미지(인라인 요소)**를 가운데 정렬할 때. 부모에 적용.

### `display: flex` vs `display: inline-flex`
- `flex` → 상자 자체가 블록처럼 가로 100% 차지
- `inline-flex` → 상자 자체가 글자처럼 내용물 크기만큼만 차지 (링크나 버튼에 유용)

### `flex-grow`
- 남은 공간을 해당 요소가 다 차지하게 늘어나도록 함
- 검색창에서 `#searchInput`에만 주고 버튼에는 주지 않음 → 버튼은 제 크기, 입력창이 나머지를 다 차지

### `flex-shrink`
- `flex-shrink: 1` (기본값): 공간이 부족하면 자동으로 찌그러짐
- `flex-shrink: 0`: 공간이 부족해도 절대 찌그러지지 않음 → 가로 스크롤 카드에 필수

### `min-height: 100vh`
- `vh`는 Viewport Height(화면 높이)의 줄임말. `100vh` = 기기 화면 높이의 100%
- 내용이 없어도 최소한 화면 전체 높이를 차지하도록 보장
- 자식 요소가 `flex-grow`로 남은 공간을 채우려면, 부모에 이 값이 설정되어 있어야 함

### 화면 전체 높이 채우는 패턴 (3단계)
```
1. .app-container   → min-height: 100vh; display: flex; flex-direction: column;
2. main             → flex-grow: 1; display: flex; flex-direction: column;
3. .favorites       → flex-grow: 1;
```
→ 3번이 1번의 남은 공간을 모두 채우게 됨

### `overflow-x: auto`
- 가로로 내용이 넘칠 때 스크롤바를 자동 생성
- 가로 스크롤 목록을 만들 때 `flex-shrink: 0`과 반드시 함께 사용
- `justify-content: center`와 함께 쓰면 첫 카드가 잘리는 버그 발생 → `flex-start`로 변경

### `gap`
- flex 컨테이너에서 자식 요소들 **사이**에만 간격을 줌 (첫/마지막 바깥에는 여백 없음)
- `margin`을 개별로 주는 것보다 훨씬 간편

### `max-width` + `width: 100%` 조합
- `max-width`: 더 이상 커지지 않을 최대 한도
- `width: 100%`: 화면이 더 작을 때 화면에 맞게 줄어들기 위한 설정
- 둘을 함께 쓰면 "큰 화면에서는 고정 크기, 작은 화면에서는 반응형"이 됨

### Jinja2 정적 파일 경로
```html
<!-- CSS -->
<link rel="stylesheet" href="{{ url_for('static', path='/css/common.css') }}">
<!-- 이미지 -->
<img src="{{ url_for('static', path='/images/logo.png') }}" alt="...">
<!-- JS -->
<script src="{{ url_for('static', path='/js/main.js') }}"></script>
```

### Jinja2 데이터 표시 (results.html, book_detail.html에서 사용)
```html
<!-- 변수 출력 -->
{{ keyword }}

<!-- 반복문 -->
{% for book in books %}
    <div>{{ book.title }}</div>
{% endfor %}

<!-- 조건문 -->
{% if not books %}
    <p>검색 결과가 없습니다.</p>
{% endif %}
```

---

## 💡 5. CSS 작업 팁

### 브라우저 개발자 도구 활용
1. Chrome에서 페이지 열기 (`http://127.0.0.1:8000`)
2. 바꾸고 싶은 요소에서 **우클릭 → 검사(Inspect)**
3. 오른쪽 패널에서 CSS 값을 **실시간으로 바꿔보며** 원하는 값 탐색
4. 마음에 드는 값을 파일에 복사

### CSS 파일 분리 기준
- `common.css` → **모든 페이지에 동일하게 쓰이는** 스타일 (헤더 로고, 검색창, 하단 탭바 등)
- `index.css` → **메인 페이지(`index.html`)에만** 쓰이는 스타일 (최근 검색, 즐겨찾기 등)
- `results.css` → 검색 결과 페이지 전용
- `book_detail.css` → 상세 페이지 전용

### 자주 헷갈리는 CSS 속성

| 속성 | 의미 | 예시 |
|---|---|---|
| `margin` | 요소 **바깥** 여백 | `margin: 10px 0` = 위아래 10px |
| `padding` | 요소 **안쪽** 여백 | `padding: 16px` = 사방 16px |
| `border-radius` | 모서리 둥글게 | `border-radius: 20px` |
| `box-shadow` | 그림자 | `box-shadow: 0 4px 12px rgba(0,0,0,0.1)` |
| `display: flex` | Flexbox 레이아웃 시작 | 자식 요소들 가로 배치 |
| `flex-direction: column` | flex 방향을 세로로 변경 | 자식 요소들 세로 배치 |
| `flex-grow: 1` | 남은 공간 채우며 늘어남 | `<main>`, `.favorites`에 사용 |
| `flex-shrink: 0` | 줄어들지 않게 고정 | 가로 스크롤 카드에 사용 |
| `gap` | flex 요소 사이 간격 | `gap: 8px` |
| `overflow-x: auto` | 가로 스크롤 | 즐겨찾기 목록에 사용 |
| `min-height: 100vh` | 최소한 화면 전체 높이 보장 | `.app-container`에 사용 |
| `CSS 태그 선택자` | 클래스 없이 태그 이름으로 스타일 지정 | `main { ... }` |

---

## ❓ 막힐 때 질문하는 방법

AI에게 구체적으로 질문할수록 더 정확한 답을 받을 수 있습니다:

> ❌ "탭바 어떻게 만들어요?"
>
> ✅ "도도리 메인 페이지에서 `common.css`에 하단 탭바(`.bottom-nav`) 스타일을 추가하려고 해요. PC 브라우저 전체 너비를 쓰고, 화면 하단에 고정되어야 해요. 탭은 5개(홈/서재/비교/탐색/MY)이고, 각 탭은 아이콘과 텍스트가 세로로 쌓이는 구조예요. 현재 선택된 탭은 파란색으로 강조돼야 해요. CSS 속성을 어떻게 설정해야 하나요?"

---

## 🤖 6. Step 6 설계 — AI 리뷰 기능 (UI 재설계 완료 후 진행)

> **상태:** ⏳ 대기 (Step 5 UI 재설계 완료 후 시작)
> **담당 파일:** `app/services/ai_service.py` (신규 생성)
> **참고 목업:** `docs/imgs/상세 페이지 - 요약.png`

### 기능 1: 리뷰 요약
- 수집된 리뷰 전체 텍스트를 Gemini API에 전달
- **출력 형식:** 장점 3개 / 단점 3개 / 핵심 키워드 태그
- 연동 위치: 상세 페이지 "요약" 탭

### 기능 2: 도서 내용 리뷰 필터링
- 수집된 리뷰 중 배송, 포장, 인쇄 품질 등 책의 내용과 **무관한 리뷰를 제외**하고 순수하게 책의 내용/퀄리티를 평가한 리뷰만 표시
- Gemini API 프롬프트로 분류 처리 (각 리뷰가 "내용 평가"인지 "기타"인지 판단)
- 연동 위치: 상세 페이지 "리뷰" 탭 내 필터 토글

### 구현 계획
```
app/services/
└── ai_service.py        ← 신규 생성
    ├── summarize_reviews(reviews: list) -> dict   # 요약 함수
    └── filter_content_reviews(reviews: list) -> list  # 필터링 함수

app/main.py
└── GET /api/books/{isbn}/ai-summary  ← 신규 엔드포인트
```

### 환경 변수
```
# .env 에 추가 필요
GEMINI_API_KEY=your_api_key_here
```

---

## 📺 7. Step 7 설계 — YouTube 연동 (Step 6 완료 후 진행)

> **상태:** ⏳ 대기 (Step 6 완료 후 시작)
> **담당 파일:** `app/services/youtube_service.py` (신규 생성)
> **연동 위치:** 상세 페이지 내 별도 섹션

### 기능
- 책 제목 + 저자 이름을 검색어로 YouTube Data API v3 호출
- 관련 영상 최대 5개의 썸네일, 제목, 채널명, 링크를 반환
- 상세 페이지에 "관련 영상" 섹션으로 표시

### 구현 계획
```
app/services/
└── youtube_service.py          ← 신규 생성
    └── search_book_videos(title: str, author: str) -> list

app/main.py
└── GET /api/books/{isbn}/videos  ← 신규 엔드포인트
```

### 환경 변수
```
# .env 에 추가 필요
YOUTUBE_API_KEY=your_api_key_here
```

### API 참고
- YouTube Data API v3 검색 엔드포인트: `https://www.googleapis.com/youtube/v3/search`
- 필요한 필드: `snippet.title`, `snippet.channelTitle`, `snippet.thumbnails`, `id.videoId`
- 무료 할당량: 일일 10,000 유닛 (검색 1회 = 100유닛 → 하루 100회 검색 가능)
