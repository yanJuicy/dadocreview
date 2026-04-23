$reviewFetchForm = document.getElementById("review-fetch-form");
$reviewList = document.getElementById("review-list");

$reviewFetchForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    // $reviewList.innerHTML = "";

    bookId = $reviewFetchForm.dataset.bookId;
    response = await fetch("/books/" + bookId + "/reviews", {
        method: "GET",
    });

    reviews = await response.json();
    console.log(reviews);
    reviews.forEach(review => {
        const reviewHtml = `
            <div class="review-item">
                <span class="review-rating">⭐ ${review.rating}</span>
                <p class="review-content">${review.content}</p>
            </div>
            `;
        $reviewList.insertAdjacentHTML("beforeend", reviewHtml);
    });
    $emptyReviewList = document.getElementById("empty-review-list");
    $emptyReviewList.style.display = "none";
    $reviewFetchForm.style.display = "none";
});

