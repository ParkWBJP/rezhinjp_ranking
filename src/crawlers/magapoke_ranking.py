import requests
from bs4 import BeautifulSoup
import json
import time

URL = "https://pocket.shonenmagazine.com/ranking/30"
BASE_URL = "https://pocket.shonenmagazine.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 1. 페이지 요청 및 파싱
resp = requests.get(URL, headers=HEADERS)
time.sleep(1)
soup = BeautifulSoup(resp.text, "html.parser")

# 2. 랭킹 리스트 추출 (상위 20개)
data = []
items = soup.select("ul.c-ranking-items > li.c-ranking-items__item")
for idx, item in enumerate(items[:20], 1):
    # 제목
    title_tag = item.select_one(".c-ranking-item__ttl")
    title = title_tag.text.strip() if title_tag else ""
    # 썸네일
    img_tag = item.select_one(".c-ranking-item__img > img")
    thumbnail = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""
    # URL
    a_tag = item.select_one("a.c-ranking-item")
    url = BASE_URL + a_tag["href"] if a_tag and a_tag.has_attr("href") else ""
    # 작가명 (예외처리)
    author = ""
    # (추후 작가명 구조가 추가되면 여기에 로직 추가)
    data.append({
        "rank": idx,
        "title": title,
        "author": author,
        "genre": "",
        "thumbnail": thumbnail,
        "url": url
    })

# 3. 저장
with open("magapoke_ranking.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(json.dumps(data, ensure_ascii=False, indent=2))

print("[완료] magapoke_ranking.json 저장됨") 