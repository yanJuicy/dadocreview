# 🎨 도도리 UI 직접 코딩 가이드

> **목표**: `docs/imgs`의 디자인 목업을 보고, `app/static`의 HTML/CSS 파일을 직접 수정해 완성하기

---

## 📁 1. 현재 파일 구조 파악

```
app/
├── templates/           ← HTML 파일들 (페이지 뼈대)
│   ├── index.html       ← 메인 홈 페이지
│   ├── results.html     ← 검색 결과 페이지
│   └── book_detail.html ← 책 상세 페이지
│
└── static/
    ├── css/             ← CSS 파일들 (스타일)
    │   ├── common.css   ← 모든 페이지 공통 스타일 (헤더, 레이아웃)
    │   ├── index.css    ← 메인 페이지 전용 스타일
    │   ├── results.css  ← 검색 결과 페이지 전용 스타일
    │   ├── book_detail.css ← 상세 페이지 전용 스타일
    │   └── style.css    ← (구버전 통합 파일 - 지금은 안 쓰임)
    │
    └── js/              ← JavaScript (동작 로직)
        ├── main.js      ← 메인 페이지 동작
        └── book_detail.js ← 상세 페이지 동작
```

> [!IMPORTANT]
> **HTML 수정 → `app/templates/`** | **스타일 수정 → `app/static/css/`**
> `style.css`는 현재 어떤 HTML에도 `<link>`되어 있지 않으므로 무시해도 됩니다.

---

## 🖼️ 2. 디자인 목업 vs 현재 코드 — 페이지별 차이점 분석

### 📌 공통 — 아직 없는 것들

목업을 보면 **하단 네비게이션 바(탭바)**가 모든 페이지에 있습니다.

```
홈 | 서재 | 비교 | 탐색 | MY
```

현재 코드에는 이 탭바가 **전혀 없습니다**. 모든 페이지 HTML에 추가해야 합니다.

---

### 📌 메인 페이지 (`index.html` + `index.css`)

**목업 이미지**: `메인 페이지.png`, `메인 페이지 - 검색.png`

| 목업에 있는 요소 | 현재 코드 상태 |
|---|---|
| 🏠 로고 + 서브타이틀 "도서관 도서 리뷰" | 로고만 있음, 서브타이틀 없음 |
| 🔍 검색창 (크고 둥근 형태) | ✅ 있음 (스타일 거의 맞음) |
| ⏰ "최근 검색" 태그 목록 | ❌ 없음 |
| ⭐ "즐겨찾기" 책 표지 가로 스크롤 | ❌ 없음 |
| 📚 "추천 도서" 목록 (카드 형식) | ❌ 없음 |
| 하단 탭 네비게이션 | ❌ 없음 |

---

### 📌 검색 결과 페이지 (`results.html` + `results.css`)

**목업 이미지**: `메인 페이지 - 검색.png` (검색 후 결과 화면)

| 목업에 있는 요소 | 현재 코드 상태 |
|---|---|
| 검색창이 상단에 유지됨 | ❌ 없음 (results.html에 검색창 없음) |
| "검색 결과" 헤더 + 권수 표시 | ✅ 거의 비슷하게 있음 |
| 책 카드 (표지 + 제목 + 저자 + 강점/약점) | 표지+제목+저자만 있음 |
| 각 카드 하단 "강남구립도서관 대출 가능" 뱃지 | ❌ 없음 |
| 하단 탭 네비게이션 | ❌ 없음 |

---

### 📌 책 상세 페이지 (`book_detail.html` + `book_detail.css`)

**목업 이미지**: `상세 페이지 - 요약.png`, `상세 페이지 - 리뷰.png`, `상세 페이지 - 목차.png`, `상세 페이지 - 상세정보.png`

| 목업에 있는 요소 | 현재 코드 상태 |
|---|---|
| 상단 뒤로가기 버튼 + 책 제목 헤더 | ❌ 없음 |
| 책 표지 + 제목 + 저자 + 출판사 + 통계(대출/보유/평점) | 표지+제목+저자+출판사만 있음 |
| "도서관 찾기" 파란 버튼 + "찜하기" 버튼 | "리뷰 가져오기" 버튼만 있음 |
| 탭 메뉴 (요약 / 상세정보 / 목차 / 리뷰) | ❌ 없음 |
| 요약 탭: AI 분석 핵심, 이래서 좋아요/참고하세요 카드 | ❌ 없음 |
| 리뷰 탭: 별점 + 리뷰어 이름 + 출처 + 날짜 | ⚠️ 별점+내용+출처만 있음 |
| 하단 탭 네비게이션 | ❌ 없음 |

---

### 📌 아직 없는 페이지들 (새로 만들어야 함)

| 페이지 | 목업 파일 |
|---|---|
| 서재 페이지 | `서재 페이지.png` |
| 탐색 페이지 | `탐색 페이지.png` |
| 비교 페이지 | `비교 페이지.png`, `비교 페이지 - 폴더 선택.png`, `비교 페이지 - 비교 표 보기.png` |

---

## 🧩 3. CSS 핵심 개념 — 꼭 알아야 할 것들

### 3-1. 색상 팔레트 (목업에서 추출)

```css
/* 현재 코드에 이미 쓰이는 색상들 */
--bg-main: #FDFBF7;        /* 배경색 (따뜻한 흰색) */
--text-dark: #333333;       /* 기본 텍스트 */
--text-gray: #888888;       /* 보조 텍스트 */

/* 목업에서 추가로 보이는 색상들 */
--blue-primary: #5B8DEF;    /* 주요 버튼 (도서관 찾기) */
--green-available: #4ECDC4; /* 대출 가능 뱃지 */
--star-yellow: #FFB800;     /* 별점 색상 */
--border-light: #EEEEEE;    /* 테두리 */
```

### 3-2. Flexbox — 가장 많이 쓰게 될 레이아웃

```css
/* 가로로 나란히 배치 */
.container {
    display: flex;
    flex-direction: row;    /* 기본값, 가로 방향 */
    gap: 10px;              /* 요소 사이 간격 */
    align-items: center;    /* 세로 중앙 정렬 */
}

/* 세로로 쌓기 */
.container {
    display: flex;
    flex-direction: column; /* 세로 방향 */
}

/* 하나가 남은 공간 다 차지하게 */
.flex-item {
    flex: 1;  /* 이 요소가 나머지 공간을 모두 차지 */
}
```

### 3-3. 가로 스크롤 목록 (즐겨찾기, 추천 도서 등)

```css
/* 가로로 스크롤되는 컨테이너 */
.horizontal-scroll {
    display: flex;
    flex-direction: row;
    overflow-x: auto;       /* 가로 스크롤 활성화 */
    gap: 12px;
    padding-bottom: 8px;    /* 스크롤바 공간 */
    /* 스크롤바 숨기기 */
    -ms-overflow-style: none;
    scrollbar-width: none;
}
.horizontal-scroll::-webkit-scrollbar {
    display: none;
}

/* 스크롤 안의 아이템은 크기 고정 */
.scroll-item {
    flex-shrink: 0;  /* 줄어들지 않게 */
    width: 100px;
}
```

### 3-4. 하단 탭바 (고정 네비게이션)

```css
.bottom-nav {
    position: fixed;        /* 화면에 고정 */
    bottom: 0;
    left: 50%;
    transform: translateX(-50%); /* 중앙 정렬 */
    width: 100%;
    max-width: 480px;
    background: #FFFFFF;
    border-top: 1px solid #EEEEEE;
    display: flex;
    justify-content: space-around; /* 탭들 균등 배치 */
    padding: 10px 0 20px 0; /* 하단 여백 (모바일 홈 버튼 고려) */
    z-index: 1000;
}

.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    color: #999;
    text-decoration: none;
}

.nav-item.active {
    color: #5B8DEF;  /* 현재 페이지 탭 강조 */
}
```

### 3-5. 탭 메뉴 (상세 페이지의 요약/상세정보/목차/리뷰)

```css
.tab-menu {
    display: flex;
    border-bottom: 1px solid #EEEEEE;
    width: 100%;
}

.tab-item {
    flex: 1;
    text-align: center;
    padding: 12px 0;
    font-size: 14px;
    color: #999;
    cursor: pointer;
    border-bottom: 2px solid transparent; /* 기본은 투명 선 */
}

.tab-item.active {
    color: #5B8DEF;
    border-bottom-color: #5B8DEF; /* 활성 탭 파란 선 */
    font-weight: 700;
}
```

---

## 🚀 4. 추천 구현 순서

CSS를 처음 다뤄본다면, **아래 순서대로** 작은 것부터 시작하세요.

### ✅ Step 1 — 하단 탭바 추가 (모든 HTML에 공통)

> 가장 먼저 하면 좋은 이유: 목업과 가장 다르게 느껴지는 부분이고, 한 번 만들면 복사-붙여넣기로 쓸 수 있음

**할 일:**
1. `common.css`에 `.bottom-nav` 스타일 추가 (위 3-4 참고)
2. `index.html`, `results.html`, `book_detail.html` 의 `</body>` 직전에 탭바 HTML 추가

```html
<!-- 모든 페이지 body 맨 아래에 추가 -->
<nav class="bottom-nav">
    <a href="/" class="nav-item active">
        <span>🏠</span>
        <span>홈</span>
    </a>
    <a href="/library" class="nav-item">
        <span>📚</span>
        <span>서재</span>
    </a>
    <a href="/compare" class="nav-item">
        <span>⚖️</span>
        <span>비교</span>
    </a>
    <a href="/explore" class="nav-item">
        <span>🔍</span>
        <span>탐색</span>
    </a>
    <a href="/my" class="nav-item">
        <span>👤</span>
        <span>MY</span>
    </a>
</nav>
```

---

### ✅ Step 2 — 메인 페이지 로고 서브타이틀 추가

> 아주 작은 변경인데 목업과 훨씬 가까워짐

**`index.html` 수정:**

```html
<!-- 현재 -->
<div class="logo">🐿️ 도도리</div>

<!-- 변경 후 -->
<div class="logo">🏠 도도리</div>
<p class="logo-subtitle">도서관 도서 리뷰</p>
```

**`common.css` 추가:**
```css
.logo-subtitle {
    font-size: 13px;
    color: #999;
    margin: 4px 0 0 0;
    font-weight: 400;
}
```

---

### ✅ Step 3 — 책 상세 페이지 탭 메뉴 추가

> 현재 페이지에서 가장 많이 쓰이고 바꾸면 티가 많이 나는 부분

**`book_detail.html`에 탭 HTML 추가:**

```html
<!-- book-detail-header 아래, detail-container 안에 추가 -->
<div class="tab-menu">
    <div class="tab-item active" onclick="showTab('summary')">요약</div>
    <div class="tab-item" onclick="showTab('info')">상세정보</div>
    <div class="tab-item" onclick="showTab('toc')">목차</div>
    <div class="tab-item" onclick="showTab('review')">리뷰</div>
</div>
```

**탭 전환 JavaScript (`book_detail.js`에 추가):**

```javascript
function showTab(tabName) {
    // 모든 탭 비활성화
    document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
    // 클릭한 탭 활성화
    event.target.classList.add('active');

    // 탭 내용 전환 (각 섹션에 id를 붙여야 함)
    document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
    document.getElementById('tab-' + tabName).style.display = 'block';
}
```

---

### ✅ Step 4 — 리뷰 카드 스타일 개선

**현재 리뷰 카드 HTML:**
```html
<div class="review-item">
    <span class="review-rating">⭐ 4.5</span>
    <p class="review-content">리뷰 내용...</p>
    <small class="review-site">출처: 교보문고</small>
</div>
```

**목업처럼 개선하려면 (리뷰어 이름, 날짜 추가):**
```html
<div class="review-item">
    <div class="review-header">
        <span class="reviewer-name">책읽는사람</span>
        <span class="review-source">교보문고</span>
        <span class="review-date">2026년 3월 15일</span>
    </div>
    <div class="review-stars">★★★★★</div>
    <p class="review-content">리뷰 내용...</p>
</div>
```

**`book_detail.css`에 추가:**
```css
.review-header {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 6px;
}

.reviewer-name {
    font-weight: 700;
    font-size: 14px;
    color: #333;
}

.review-source {
    font-size: 11px;
    color: #999;
    background: #F5F5F5;
    padding: 2px 6px;
    border-radius: 4px;
}

.review-date {
    font-size: 12px;
    color: #aaa;
    margin-left: auto; /* 오른쪽 끝으로 밀기 */
}

.review-stars {
    color: #FFB800;
    font-size: 14px;
    margin-bottom: 6px;
}
```

---

## 🆕 5. 새로 만들어야 할 페이지

목업에 있지만 HTML 파일이 없는 페이지들입니다. 백엔드(Python) 라우트도 함께 추가해야 합니다.

| 파일 | 목업 | 설명 |
|---|---|---|
| `templates/library.html` | `서재 페이지.png` | 나만의 책장, 폴더별 책 목록 |
| `templates/explore.html` | `탐색 페이지.png` | 베스트셀러, 신간, 카테고리 탐색 |
| `templates/compare.html` | `비교 페이지.png` | 비교 폴더 목록 |
| `templates/compare_detail.html` | `비교 페이지 - 폴더 선택.png`, `비교 페이지 - 비교 표 보기.png` | 폴더 상세 + 비교표 |

> [!NOTE]
> 새 페이지는 HTML부터 만들고 → CSS를 `common.css`에 추가하거나 새 CSS 파일을 만들어 link하는 방식으로 진행하세요.

---

## 💡 6. CSS 작업 팁 — 처음이라면

### 브라우저 개발자 도구 활용
1. Chrome/Safari에서 페이지 열기
2. 수정하고 싶은 요소에서 **우클릭 → 검사(Inspect)**
3. 오른쪽 패널에서 CSS 값을 **실시간으로 변경**해보며 값 확인
4. 마음에 드는 값을 파일에 복사

### 자주 헷갈리는 CSS 속성

| 속성 | 의미 | 예시 |
|---|---|---|
| `margin` | 요소 **바깥** 여백 | `margin: 10px 0` = 위아래 10px |
| `padding` | 요소 **안쪽** 여백 | `padding: 16px` = 사방 16px |
| `border-radius` | 모서리 둥글게 | `border-radius: 12px` |
| `box-shadow` | 그림자 | `box-shadow: 0 4px 12px rgba(0,0,0,0.1)` |
| `display: flex` | Flexbox 레이아웃 시작 | 자식 요소들 나란히 배치 |
| `gap` | flex/grid 요소 사이 간격 | `gap: 16px` |
| `overflow: hidden` | 넘치는 내용 숨기기 | 카드 내용이 삐져나오면 사용 |

### 색상 표현 방법

```css
/* 16진수 */
color: #333333;

/* rgba (투명도 조절 가능) */
background: rgba(0, 0, 0, 0.1);  /* 10% 불투명 검정 */

/* 그라디언트 (탐색 페이지 헤더처럼) */
background: linear-gradient(135deg, #667eea, #764ba2);
```

---

## 📋 7. 작업 체크리스트

### 우선순위 높음 (지금 바로 가능)
- [ ] `common.css` — 하단 탭바(`.bottom-nav`) 스타일 추가
- [ ] 모든 HTML — 탭바 HTML 추가
- [ ] `index.html` — 로고 서브타이틀 추가
- [ ] `book_detail.html` — 탭 메뉴(요약/상세정보/목차/리뷰) HTML 추가
- [ ] `book_detail.css` — 탭 메뉴 스타일 추가

### 우선순위 중간 (현재 페이지 개선)
- [ ] `index.html` — "최근 검색" 태그 섹션 추가
- [ ] `index.html` — "즐겨찾기" 가로 스크롤 섹션 추가
- [ ] `results.html` — 대출 가능 뱃지 추가
- [ ] `book_detail.html` — 책 통계(대출수/보유수/평점) 추가
- [ ] `book_detail.html` — "도서관 찾기" / "찜하기" 버튼 추가

### 우선순위 낮음 (새 페이지 생성)
- [ ] `library.html` 생성 — 서재 페이지
- [ ] `explore.html` 생성 — 탐색 페이지  
- [ ] `compare.html` 생성 — 비교 페이지
- [ ] `compare_detail.html` 생성 — 비교 폴더 상세 + 비교표

---

## ❓ 막힐 때 질문하는 방법

AI에게 물어볼 때 이렇게 구체적으로 질문하면 더 좋은 답을 받을 수 있어요:

> ❌ "탭바 어떻게 만들어요?"
>
> ✅ "도도리 앱에서 `common.css`에 하단 탭바 스타일을 추가하려는데, 화면 하단에 고정되고 최대 너비가 480px로 제한되어야 해요. 탭은 5개(홈/서재/비교/탐색/MY)이고, 현재 탭은 파란색으로 강조해야 해요. CSS 코드를 보여주세요."
