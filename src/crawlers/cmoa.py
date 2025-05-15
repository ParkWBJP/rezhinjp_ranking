import requests
from bs4 import BeautifulSoup
import json
import re

BASE_URL = "https://www.cmoa.jp/search/purpose/ranking/all/"
SITE_URL = "https://www.cmoa.jp"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
}

def get_cmoa_top20():
    res = requests.get(BASE_URL, headers=HEADERS, timeout=10)
    if res.status_code != 200:
        print(f"시모아 페이지 요청 실패: {res.status_code}")
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select("li.search_result_box")
    result = []
    for idx, item in enumerate(items[:20], 1):
        try:
            # 썸네일
            img = item.select_one("img.volume_img")
            thumbnail = "https:" + img["src"] if img and img.get("src") else ""
            # 제목/상세URL
            title_tag = item.select_one("div.search_result_box_right_sec1 a.title")
            title = title_tag.text.strip() if title_tag else ""
            url = SITE_URL + title_tag["href"] if title_tag and title_tag.get("href") else ""
            # 작가
            author_tag = item.select_one("p:has(a[href*='/search/author/'])")
            author = author_tag.a.text.strip() if author_tag and author_tag.a else ""
            # 장르
            genre_tag = item.select_one("p:has(a[href*='/search/genre/'])")
            genre = genre_tag.a.text.strip() if genre_tag and genre_tag.a else ""
            # 별점 및 참여수
            review = item.select_one("div.review_value")
            rating = None
            rating_count = None
            if review:
                m = re.search(r'（([0-9.]+)）', review.text)
                if m:
                    rating = float(m.group(1))
                m2 = re.search(r'投稿数(\d+)件', review.text.replace(',', ''))
                if m2:
                    rating_count = int(m2.group(1))
            result.append({
                "rank": idx,
                "title": title,
                "author": author,
                "genre": genre,
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
    data = get_cmoa_top20()
    with open("frontend/public/cmoa_sample.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved to frontend/public/cmoa_sample.json") 