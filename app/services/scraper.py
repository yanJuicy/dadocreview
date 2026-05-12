from requests import request
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, Timeout


def get_kyobo_book_id(isbn):
    url = f"https://search.kyobobook.co.kr/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    params = {
        "keyword": isbn,
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
    except HTTPError as e:
        print(f"HTTP Error: {e}")
        return None
    except Timeout as e:
        print(f"Timeout Error: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")  # soup 준비
    for a_tag in soup.find_all("a", href=True):
        link = a_tag["href"]
        if "https://product.kyobobook.co.kr/detail" in link:
            book_id = link.split("/")[-1]
            return book_id
    return None


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

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
    except HTTPError as e:
        print(f"HTTP Error: {e}")
        return []
    except Timeout as e:
        print(f"Timeout Error: {e}")
        return []

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
    if book_id is None:
        return []
    reviews = fetch_kyobo_book_reviews(book_id)
    return reviews


def fetch_yes24_goods_id(isbn):
    url = f"https://www.yes24.com/product/search"
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    # }
    params = {
        "query": isbn,
        "domain": "BOOK"
    }
    try:
        # response = requests.get(url, headers=headers, params=params, timeout=5)
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
    except HTTPError as e:
        print(f"HTTP Error: {e}")
        return None
    except Timeout as e:
        print(f"Timeout Error: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    print(soup)
    # for a_tag in soup.find_all("a", href=True):
    #     print(a_tag)

    # 'class_' 파라미터를 사용하면 클래스가 없는 태그도 안전하게 건너뛰며 필터링할 수 있습니다.
    for a_tag in soup.find_all("a", class_="gd_name"):
        print(a_tag)
        # ID를 추출하려면 아래와 같이 처리할 수 있습니다.
        href = a_tag.get("href", "")
        if "/product/goods/" in href:
            return href.split("/")[-1]
    return None


def fetch_yes24_review(goods_id):
    pass


def get_yes24_reviews(isbn):
    pass



if __name__ == "__main__":
    # 테스트용 교보문고 책 ID (아까 확인한 '파이썬' 관련 책 ID)
    test_isbn = "9788925588735"

    # 함수를 호출해서 결과 받아보기
    result = fetch_yes24_goods_id(test_isbn)

    # 결과 출력해보기
    print(result)
