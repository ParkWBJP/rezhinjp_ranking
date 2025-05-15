import requests
from bs4 import BeautifulSoup
import json
import time

URL = "https://booklive.jp/ranking/day/category_id/C"
BASE_URL = "https://booklive.jp"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

resp = requests.get(URL, headers=HEADERS)
time.sleep(1)
soup = BeautifulSoup(resp.text, "html.parser")

data = []
items = soup.select("ul.search_item_list > li.item")
for idx, item in enumerate(items[:20], 1):
    # 제목
    title_tag = item.select_one("div.title h3.inline a")
    title = title_tag.text.strip() if title_tag else ""
    # 작가 (여러 명일 수 있음)
    author_tags = item.select("div.spec_list > div.spec:nth-child(1) .detail_item a")
    author = ", ".join([a.text.strip() for a in author_tags]) if author_tags else ""
    # 장르
    genre_tag = item.select_one("div.spec_list > div.spec:nth-child(2) .detail_item span")
    genre = genre_tag.text.strip() if genre_tag else ""
    # 썸네일
    img_tag = item.select_one("div.left .picture img")
    thumbnail = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""
    # 상세 URL
    url = BASE_URL + title_tag["href"] if title_tag and title_tag.has_attr("href") else ""
    # 설명
    desc_tag = item.select_one("div.multi_line_txt")
    description = desc_tag.text.strip() if desc_tag else ""
    # 리뷰 수(참여 수) - BookLive는 랭킹 리스트에 리뷰 수가 없으므로 0으로
    review_count = 0
    data.append({
        "rank": idx,
        "title": title,
        "author": author,
        "genre": genre,
        "thumbnail": thumbnail,
        "url": url,
        "description": description,
        "review_count": review_count
    })

with open("booklive_ranking.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(json.dumps(data, ensure_ascii=False, indent=2))

print("[완료] booklive_ranking.json 저장됨") 