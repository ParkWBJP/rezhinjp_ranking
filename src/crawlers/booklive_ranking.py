import requests
from bs4 import BeautifulSoup
import json
import shutil
import time

URL = "https://booklive.jp/ranking/day"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

resp = requests.get(URL, headers=HEADERS)
time.sleep(1)
soup = BeautifulSoup(resp.text, "html.parser")

# HTML 저장 (디버깅용)
with open("booklive_debug.html", "w", encoding="utf-8") as f:
    f.write(resp.text)

# BookLive 랭킹 리스트 파싱 (li.item 기준)
data = []
items = soup.select("li.item")
for idx, item in enumerate(items[:20], 1):
    # 제목
    title_tag = item.select_one("h3.inline a")
    title = title_tag.text.strip() if title_tag else ""
    
    # 썸네일
    img_tag = item.select_one("div.picture img")
    thumbnail = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""
    
    # URL
    a_tag = item.select_one("div.picture a")
    url = a_tag["href"] if a_tag and a_tag.has_attr("href") else ""
    if url and not url.startswith("http"):
        url = "https://booklive.jp" + url
    
    # 작가명
    author_tag = item.select_one("div.spec_list div.spec:first-child .detail_item")
    author = author_tag.text.strip() if author_tag else ""
    
    # 장르
    genre_tag = item.select_one("div.spec_list div.spec:nth-child(2) .detail_item")
    genre = genre_tag.text.strip() if genre_tag else ""
    
    data.append({
        "rank": idx,
        "title": title,
        "author": author,
        "genre": genre,
        "thumbnail": thumbnail,
        "url": url
    })

with open("booklive_ranking.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(json.dumps(data, ensure_ascii=False, indent=2))

print("[완료] booklive_ranking.json 저장됨")

# 크롤링 결과를 frontend/public 폴더로 자동 복사
try:
    shutil.copy("booklive_ranking.json", "frontend/public/booklive_ranking.json")
    print("✅ 최신 booklive_ranking.json이 frontend/public 폴더로 복사되었습니다.")
except Exception as e:
    print(f"⚠️ public 폴더 복사 중 에러: {e}") 