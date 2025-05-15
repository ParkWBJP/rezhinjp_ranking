import requests
from bs4 import BeautifulSoup
import json
import re

BASE_URL = "https://renta.papy.co.jp/renta/sc/frm/search?word=&type=desc&span=d&sort=rank&site_type=c&detail=on"
SITE_URL = "https://renta.papy.co.jp"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
}

def get_renta_top20():
    res = requests.get(BASE_URL, headers=HEADERS, timeout=10)
    if res.status_code != 200:
        print(f"Renta 페이지 요청 실패: {res.status_code}")
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select("li.desclist-item")
    result = []
    for idx, item in enumerate(items[:20], 1):
        try:
            # 썸네일
            img = item.select_one("div.c-contents_coverwrap img.c-contents_cover")
            thumbnail = img.get("data-src") or img.get("src") if img else ""
            # 제목/상세URL
            title_tag = item.select_one("h2.desclist-title a.desclist-title_link")
            title = title_tag.text.strip() if title_tag else ""
            url = SITE_URL + title_tag["href"] if title_tag and title_tag.get("href") else ""
            # 작가
            author_tag = item.select_one("li:has(a[href*='author='])")
            author = author_tag.a.text.strip() if author_tag and author_tag.a else ""
            # 장르
            genre_tag = item.select_one("li:has(a[href*='genre='])")
            genre = genre_tag.a.text.strip() if genre_tag and genre_tag.a else ""
            # 별점(이미지 alt)
            rating = None
            rating_img = item.select_one("span.bst_info img[alt]")
            if rating_img and rating_img.get("alt"):
                try:
                    rating = float(rating_img["alt"])
                except:
                    rating = None
            # 참여수
            rating_count = None
            review_tag = item.select_one("span.list_review a")
            if review_tag and review_tag.text:
                try:
                    rating_count = int(review_tag.text.replace(',', ''))
                except:
                    rating_count = None
            # 무료화수
            free_tag = item.select_one("a.c-btn_free span")
            episode_count = None
            if free_tag and free_tag.text:
                m = re.search(r"(\d+)", free_tag.text)
                if m:
                    episode_count = int(m.group(1))
            result.append({
                "rank": idx,
                "title": title,
                "author": author,
                "genre": genre,
                "rating": rating,
                "rating_count": rating_count,
                "episode_count": episode_count,
                "thumbnail": thumbnail,
                "url": url,
            })
        except Exception as e:
            print(f"{idx}위 파싱 실패: {e}")
            continue
    return result

if __name__ == "__main__":
    data = get_renta_top20()
    with open("frontend/public/renta_sample.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved to frontend/public/renta_sample.json") 