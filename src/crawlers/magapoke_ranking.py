import requests
from bs4 import BeautifulSoup
import json
import shutil
import time

URL = "https://pocket.shonenmagazine.com/ranking/30"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

resp = requests.get(URL, headers=HEADERS)
time.sleep(1)
soup = BeautifulSoup(resp.text, "html.parser")

# HTML 저장 (디버깅용)
with open("magapoke_debug.html", "w", encoding="utf-8") as f:
    f.write(resp.text)

# 마가포케 랭킹 리스트 파싱 (실제 구조)
data = []
items = soup.select("ul.c-ranking-items > li.c-ranking-items__item")
for idx, item in enumerate(items[:20], 1):
    # 제목
    title_tag = item.select_one("h3.c-ranking-item__ttl")
    title = title_tag.text.strip() if title_tag else ""
    
    # URL
    a_tag = item.select_one("a.c-ranking-item")
    url = a_tag["href"] if a_tag and a_tag.has_attr("href") else ""
    if url and not url.startswith("http"):
        url = "https://pocket.shonenmagazine.com" + url
    
    # 썸네일
    img_tag = item.select_one("div.c-ranking-item__img > img")
    thumbnail = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""
    
    # 간단 설명
    intro_tag = item.select_one("p.c-ranking-item__intro")
    intro = intro_tag.text.strip() if intro_tag else ""
    
    # 상세 설명
    desc_tag = item.select_one("p.c-ranking-item__description")
    description = desc_tag.text.strip() if desc_tag else ""
    
    data.append({
        "rank": idx,
        "title": title,
        "author": "",
        "genre": "",
        "thumbnail": thumbnail,
        "url": url,
        "intro": intro,
        "description": description
    })

with open("magapoke_ranking.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(json.dumps(data, ensure_ascii=False, indent=2))

print("[완료] magapoke_ranking.json 저장됨")

# 크롤링 결과를 frontend/public 폴더로 자동 복사
try:
    shutil.copy("magapoke_ranking.json", "frontend/public/magapoke_ranking.json")
    print("✅ 최신 magapoke_ranking.json이 frontend/public 폴더로 복사되었습니다.")
except Exception as e:
    print(f"⚠️ public 폴더 복사 중 에러: {e}") 