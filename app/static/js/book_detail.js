const $reviewFetchForm = document.getElementById("review-fetch-form");
const $reviewList = document.getElementById("review-list");

// 리뷰 가져오기 버튼 클릭 이벤트
$reviewFetchForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const bookId = $reviewFetchForm.dataset.bookId;

    try {
        const response = await fetch("/books/" + bookId + "/reviews", {
            method: "GET",
        });

        if (!response.ok) {
            alert("리뷰 정보를 가져오지 못했습니다.");
            return;
        }

        const reviews = await response.json();
        reviews.forEach(review => {
            const reviewHtml = `
            <div class="review-item">
                <span class="review-rating">⭐ ${review.rating}</span>
                <p class="review-content">${review.content}</p>
            </div>
            `;
            $reviewList.insertAdjacentHTML("beforeend", reviewHtml);
        });
        const $emptyReviewList = document.getElementById("empty-review-list");
        $emptyReviewList.style.display = "none";
        $reviewFetchForm.style.display = "none";
    } catch (error) {
        alert("네트워크 오류가 발생했습니다.");
    }

});

