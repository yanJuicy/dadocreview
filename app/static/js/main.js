const $searchBtn = document.getElementById('searchBtn');
const $searchInput = document.getElementById('searchInput');

$searchBtn.addEventListener('click', () => {
    const keyword = $searchInput.value;
    if (keyword) {
        window.location.href = `/results?q=${keyword}`;
    }
});

$searchInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        const keyword = $searchInput.value;
        if (keyword) {
            window.location.href = `/results?q=${keyword}`;
        }
    }
});