import requests
import json

URL = "https://api.toptoon.jp/api/v2/daily/allByType"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

if __name__ == "__main__":
    response = requests.post(URL, headers=HEADERS, json={})
    # print(response.text)  # 응답 원문 출력 (삭제)
    data = response.json()
    result = []
    data_field = data.get("data")
    items = []
    if isinstance(data_field, list):
        items = data_field
    elif isinstance(data_field, dict):
        # 딕셔너리의 값 중 리스트인 것 찾기
        for v in data_field.values():
            if isinstance(v, list):
                items = v
                break
    for item in items:
        if not isinstance(item, dict):
            continue
        title = item.get("information", {}).get("title", "")
        abt = item.get("authorByType", {})
        authors = set(abt.get("writer", []) + abt.get("illustrator", []))
        author = ", ".join(authors)
        thumbnail = ""
        tvt = item.get("titleVerticalThumbnail", {}).get("webp", [])
        if tvt and isinstance(tvt, list) and len(tvt) > 0:
            thumbnail = tvt[0].get("path", "")
        else:
            ti = item.get("thumbnailImage", {}).get("webp", [])
            if ti and isinstance(ti, list) and len(ti) > 0:
                thumbnail = ti[0].get("path", "")
        landing_url = "https://toptoon.jp/episode/" + str(item.get("firstEpisodeId", ""))
        genre = ", ".join(item.get("keywords", []))
        like_count = item.get("information", {}).get("likeCount", 0)
        result.append({
            "title": title,
            "author": author,
            "thumbnail": thumbnail,
            "url": landing_url,
            "genre": genre,
            "like_count": like_count
        })
    with open("frontend/public/toptoon_sample.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Saved to frontend/public/toptoon_sample.json") 