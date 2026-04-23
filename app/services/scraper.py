import requests
from bs4 import BeautifulSoup


def get_kyobo_book_id(isbn):
    url = f"https://search.kyobobook.co.kr/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    params = {
        "keyword": isbn,
    }
    response = requests.get(url, headers=headers, params=params)

    soup = BeautifulSoup(response.text, "html.parser")  # soup 준비
    for a_tag in soup.find_all("a", href=True):
        link = a_tag["href"]
        if "https://product.kyobobook.co.kr/detail" in link:
            book_id = link.split("/")[-1]
            return book_id


def fetch_kyobo_book_reviews(kyobo_book_id):
    params = {
        "page": 1,
        "pageLimit": 10,
        "revwPatrCode": "000",  # 전체 리뷰
        "reviewSort": "002",  # 최신순 정렬 코드
        "saleCmdtid": kyobo_book_id,  # 교보문고 책 ID
    }
    # 브라우저인 척 하기 위한 정보(headers)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url = f"https://product.kyobobook.co.kr/api/review/list"

    response = requests.get(url, params=params, headers=headers)

    reviews_raw = response.json().get("data", {}).get("reviewList", [])
    reviews = []

    for r in reviews_raw:
        content = r.get("revwCntt")
        rating = r.get("revwRvgr")
        review_id = r.get("revwNum")  # 교보문고 고유 리뷰 번호
        reviews.append(
            {
                "content": content,
                "rating": rating,
                "source_review_id": review_id,
                "source_site": "kyobo",
            }
        )

    return reviews


def get_kyobo_reviews(isbn):
    book_id = get_kyobo_book_id(isbn)
    reviews = fetch_kyobo_book_reviews(book_id)
    return reviews


if __name__ == "__main__":
    # 테스트용 교보문고 책 ID (아까 확인한 '파이썬' 관련 책 ID)
    test_isbn = "9791130635712"

    # 함수를 호출해서 결과 받아보기
    result = get_kyobo_book_id(test_isbn)

    # 결과 출력해보기
    print(result)
