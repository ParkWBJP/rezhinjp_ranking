import requests

URL = "https://www.lezhin.jp/ja/ranking?genre=_all&rankType=realtime&filter=all"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

if __name__ == "__main__":
    response = requests.get(URL, headers=HEADERS)
    with open("lezhin_ranking_raw.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("HTML 저장 완료: lezhin_ranking_raw.html") 