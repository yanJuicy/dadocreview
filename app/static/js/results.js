const $searchBtn = document.getElementById('searchBtn');
const $searchInput = document.getElementById('searchInput');

// 검색 버튼을 클릭할 때 이벤트
$searchBtn.addEventListener('click', () => {
    const keyword = $searchInput.value.trim();
    if (keyword) {
        window.location.href = `/results?q=${encodeURIComponent(keyword)}`;
    }
});

// 검색창에서 엔터를 입력할 때 이벤트
$searchInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        const keyword = $searchInput.value.trim();
        if (keyword) {
            window.location.href = `/results?q=${encodeURIComponent(keyword)}`;
        }
    }
});
