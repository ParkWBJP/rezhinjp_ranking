import requests
from bs4 import BeautifulSoup
import json
import re

BASE_URL = "https://mechacomic.jp/sales_rankings/current"
SITE_URL = "https://mechacomic.jp"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
}

def get_mechacomic_top20():
    res = requests.get(BASE_URL, headers=HEADERS, timeout=10)
    if res.status_code != 200:
        print(f"메챠코믹 페이지 요청 실패: {res.status_code}")
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    ranking_items = soup.select("li.p-bookList_item")
    if not ranking_items or len(ranking_items) < 1:
        print("메챠코믹 랭킹 구조 변경 또는 데이터 부족!")
        return []
    result = []
    for idx, item in enumerate(ranking_items[:20], 1):
        try:
            # 썸네일
            img = item.select_one("div.p-book_jacket img.jacket_image_l")
            thumbnail = img["src"] if img else ""
            # 제목/상세URL
            title_tag = item.select_one("dt.p-book_title a")
            title = title_tag.text.strip() if title_tag else ""
            url = SITE_URL + title_tag["href"] if title_tag else ""
            # 작가
            author_tag = item.select_one("dd.p-book_author")
            author = author_tag.text.strip() if author_tag else ""
            # 장르(여러개)
            genre_tags = item.select("dd.p-tagList span.c-tag")
            genres = [g.text.strip() for g in genre_tags]
            genre = ", ".join(genres)
            # 별점
            rating_tag = item.select_one("dd.p-book_review span.p-book_average")
            rating = float(rating_tag.text.strip()) if rating_tag else None
            # 별점 참여수
            rating_count_tag = item.select_one("dd.p-book_review span.u-inlineBlock")
            rating_count = None
            if rating_count_tag and rating_count_tag.text:
                m = re.search(r"(\d+)", rating_count_tag.text.replace(',', ''))
                if m:
                    rating_count = int(m.group(1))
            # 무료화수
            free_tag = item.select_one("div.btn_free a")
            episode_count = None
            if free_tag and free_tag.text.strip():
                m = re.search(r"(\d+)話無料", free_tag.text)
                if m:
                    episode_count = int(m.group(1))
            result.append({
                "rank": idx,
                "title": title,
                "author": author,
                "genre": genre,
                "episode_count": episode_count,
                "rating": rating,
                "rating_count": rating_count,
                "thumbnail": thumbnail,
                "url": url,
            })
        except Exception as e:
            print(f"{idx}위 파싱 실패: {e}")
            continue
    return result

if __name__ == "__main__":
    data = get_mechacomic_top20()
    with open("frontend/public/mecha_sample.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved to frontend/public/mecha_sample.json") 