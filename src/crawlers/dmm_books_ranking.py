import requests
from bs4 import BeautifulSoup
import json
import time

RANKING_URL = "https://book.dmm.com/ranking/?floor=Gcomic&type=58"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
}

if __name__ == "__main__":
    URL = "https://book.dmm.com/list/?floor=Gcomic&sort=ranking"
    res = requests.get(URL, headers=HEADERS)
    res.encoding = res.apparent_encoding
    with open("dmm_books_ranking_raw.html", "w", encoding="utf-8") as f:
        f.write(res.text)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select("li.m-boxListBookProduct2__item")
    print(f"items 개수: {len(items)}")
    result = []
    for idx, item in enumerate(items[:20], 1):
        # 제목
        title_tag = item.select_one("span.m-boxListBookProduct2Tmb__ttl")
        title = title_tag.text.strip() if title_tag else ""
        # 썸네일
        img_tag = item.select_one("img.m-bookImage__img")
        thumbnail = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""
        # 작가
        author_tags = item.select("span.m-boxListBookProductTmbInfo__authorTxt a")
        author = ", ".join([a.text.strip() for a in author_tags])
        # 랜딩 URL
        a_tag = item.select_one("a.fn-addI3Parameters")
        url = a_tag["href"] if a_tag and a_tag.has_attr("href") else ""
        if url and not url.startswith("http"):
            url = "https://book.dmm.com" + url
        # 별점/리뷰수
        star_tag = item.select_one("div.react-review-star-parts-root")
        rating = star_tag["data-evaluate-average"] if star_tag and star_tag.has_attr("data-evaluate-average") else ""
        review_count = star_tag["data-post-count"] if star_tag and star_tag.has_attr("data-post-count") else ""
        # 상세페이지에서 장르 추출
        genres = []
        try:
            detail_res = requests.get(url, headers=HEADERS)
            detail_res.encoding = detail_res.apparent_encoding
            detail_soup = BeautifulSoup(detail_res.text, "html.parser")
            genres = [a.text.strip() for a in detail_soup.select('a[data-testid="genre-link"]')]
            time.sleep(0.5)
        except Exception as e:
            pass
        result.append({
            "title": title,
            "thumbnail": thumbnail,
            "author": author,
            "url": url,
            "rating": rating,
            "review_count": review_count,
            "genres": genres
        })
    with open("frontend/public/dmm_sample.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Saved to frontend/public/dmm_sample.json") 