from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

URL = "https://www.comico.jp/menu/all_comic/ranking"
BASE_URL = "https://www.comico.jp"
CHROME_PATH = r"C:\\Users\\wisebirds\\Downloads\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')

# 1. Selenium으로 페이지 완전 로딩 후 HTML 저장
service = Service(executable_path=CHROME_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(URL)
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.comicList__info"))
    )
except Exception as e:
    print(f"⚠️ 페이지 로딩 대기 중 오류: {e}")

with open("comico_selenium_result.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)
driver.quit()

# 2. BeautifulSoup으로 데이터 파싱 및 추출
HTML_PATH = "comico_selenium_result.html"
data = []
try:
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select('a[href^="/comic/"]')
    print(f"items 개수: {len(items)}")
    if not items:
        print("⚠️ 데이터 없음")
    for idx, a_tag in enumerate(items[:20], 1):
        # url
        url = a_tag.get("href", "")
        if url and not url.startswith("http"):
            url = BASE_URL + url
        # 썸네일
        thumbnail = ""
        img_tag = a_tag.select_one("img")
        if img_tag and img_tag.has_attr("src"):
            thumbnail = img_tag["src"]
        # title
        title = ""
        title_tag = a_tag.select_one(".txt-title")
        if title_tag:
            title = title_tag.text.strip()
        elif img_tag and img_tag.has_attr("alt"):
            title = img_tag["alt"].strip()
        # genre (여러 개일 수 있음)
        genre = ""
        genre_tags = a_tag.select(".txt-sub, .txt-sub span")
        if genre_tags:
            genre = ", ".join([g.text.strip() for g in genre_tags if g.text.strip()])
        # author (여러 개일 수 있음)
        author = ""
        author_tags = a_tag.select(".txt-sub2, .txt-sub2 span")
        if author_tags:
            author = ", ".join([a.text.strip() for a in author_tags if a.text.strip()])
        print(f"{idx}: rank={idx}, title={title}, author={author}, genre={genre}, thumbnail={thumbnail}, url={url}")
        data.append({
            "rank": idx,
            "title": title,
            "author": author,
            "genre": genre,
            "thumbnail": thumbnail,
            "url": url
        })
except Exception as e:
    print(f"⚠️ 에러 발생: {e}")

print(json.dumps(data, ensure_ascii=False, indent=2)) 

# 추출 데이터 JSON 파일로 저장
with open("comico_ranking.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2) 