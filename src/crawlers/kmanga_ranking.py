import requests
from bs4 import BeautifulSoup
import json
import time
import shutil

URL = "https://comic.k-manga.jp/rank/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 1. 페이지 요청 및 파싱
resp = requests.get(URL, headers=HEADERS)
time.sleep(1)
soup = BeautifulSoup(resp.text, "html.parser")

# 2. 랭킹 리스트 추출 (상위 20개)
data = []
items = soup.select("ul.book-list.book-list__one-column.book-list-ranking > li.book-list--target")
for idx, item in enumerate(items[:20], 1):
    # 제목
    title_tag = item.select_one("h2.book-list--title")
    title = title_tag.text.strip() if title_tag else ""
    # 썸네일
    img_tag = item.select_one("img.book-list--img")
    thumbnail = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""
    # URL
    a_tag = item.select_one("a.book-list--item")
    url = a_tag["href"] if a_tag and a_tag.has_attr("href") else ""
    # 작가명 (여러 명일 수 있음)
    author_tags = item.select("p.book-list--author span.book-list--author-item")
    author = ", ".join([a.text.strip() for a in author_tags]) if author_tags else ""
    # 장르 (여러 개일 수 있음)
    genre_tags = item.select("div.book-list--category-genre aside.icon-text__genre")
    genre = ", ".join([g.text.strip() for g in genre_tags]) if genre_tags else ""
    # 리뷰 수(まんがレポ)
    review_tag = item.select_one("div.book-list--repo-num span.ml2.f12")
    review_count = int(review_tag.text.strip()) if review_tag and review_tag.text.strip().isdigit() else 0
    data.append({
        "rank": idx,
        "title": title,
        "author": author,
        "genre": genre,
        "thumbnail": thumbnail,
        "url": url,
        "review_count": review_count
    })

# 3. 저장
with open("kmanga_ranking.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(json.dumps(data, ensure_ascii=False, indent=2))

print("[완료] kmanga_ranking.json 저장됨")

# 크롤링 결과를 frontend/public 폴더로 자동 복사
try:
    shutil.copy("kmanga_ranking.json", "frontend/public/kmanga_ranking.json")
    print("✅ 최신 kmanga_ranking.json이 frontend/public 폴더로 복사되었습니다.")
except Exception as e:
    print(f"⚠️ public 폴더 복사 중 에러: {e}") 