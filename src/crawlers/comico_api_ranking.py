import requests
import json
import time

BASE_URL = "https://www.comico.jp/comic/"
API_BASE = "https://lcs.comico.jp/m?u=comicoJpWeb"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.comico.jp/",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.comico.jp",
    "Connection": "keep-alive"
}
PARAMS = "&DID=web&LNG=ja-JP"

# Step 1: 랭킹 카테고리 목록 가져오기
def get_categories():
    url = f"{API_BASE}/menu/all_comic/ranking{PARAMS}"
    resp = requests.get(url, headers=HEADERS)
    print("[DEBUG] get_categories status:", resp.status_code)
    print("[DEBUG] get_categories response (앞부분):", resp.text[:500])
    resp.raise_for_status()
    data = resp.json()
    categories = []
    for item in data.get("data", {}).get("menu", {}).get("items", []):
        label = item.get("label", "")
        code = item.get("code", "")
        apiPath = item.get("apiPath", "")
        if apiPath:
            categories.append({"label": label, "code": code, "apiPath": apiPath})
    return categories

# Step 2: 각 apiPath별 랭킹 리스트 가져오기
def get_ranking_list(apiPath):
    url = f"{API_BASE}{apiPath}{PARAMS}"
    resp = requests.get(url, headers=HEADERS)
    print(f"[DEBUG] get_ranking_list({apiPath}) status:", resp.status_code)
    print(f"[DEBUG] get_ranking_list({apiPath}) response (앞부분):", resp.text[:500])
    resp.raise_for_status()
    data = resp.json()
    contents = data.get("data", {}).get("contents", [])
    result = []
    for idx, item in enumerate(contents[:20], 1):
        id_ = item.get("id")
        title = item.get("title", "")
        thumbnails = item.get("thumbnails", [])
        thumbnail = thumbnails[0]["url"] if thumbnails else ""
        episodeId = item.get("episodeId", id_)
        result.append({
            "rank": idx,
            "id": id_,
            "title": title,
            "thumbnail": thumbnail,
            "episodeId": episodeId
        })
    return result

# Step 3: 각 작품 상세 정보 가져오기
def get_detail(id_):
    url = f"{API_BASE}/comic&episodeId={id_}"
    resp = requests.get(url, headers=HEADERS)
    print(f"[DEBUG] get_detail({id_}) status:", resp.status_code)
    print(f"[DEBUG] get_detail({id_}) response (앞부분):", resp.text[:500])
    resp.raise_for_status()
    data = resp.json()
    episode = data.get("data", {}).get("episode", {})
    content = episode.get("content", {})
    authors = episode.get("authors", [])
    return {
        "title": content.get("name", ""),
        "author": ", ".join([a.get("name", "") for a in authors]),
        "description": content.get("description", ""),
        "thumbnail": content.get("thumbnails", [{}])[0].get("url", ""),
        "type": content.get("type", ""),
        "id": content.get("id", id_),
    }

def main():
    categories = get_categories()
    seen_ids = set()
    data = []
    for cat in categories:
        print(f"[INFO] 카테고리: {cat['label']} ({cat['apiPath']})")
        ranking = get_ranking_list(cat["apiPath"])
        for item in ranking:
            if item["id"] in seen_ids:
                continue
            seen_ids.add(item["id"])
            detail = get_detail(item["id"])
            data.append({
                "rank": item["rank"],
                "title": detail["title"] or item["title"],
                "author": detail["author"],
                "description": detail["description"],
                "thumbnail": detail["thumbnail"] or item["thumbnail"],
                "url": f"{BASE_URL}{item['id']}",
                "category": cat["label"]
            })
            print(f"  - {item['rank']}: {detail['title']}")
            time.sleep(1)
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 