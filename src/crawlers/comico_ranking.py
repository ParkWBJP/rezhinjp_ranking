from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import shutil

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
    ranking_items = soup.select('li[data-v-fd22c8bb]')  # 랭킹 리스트의 li만 한정
    print(f"ranking_items 개수: {len(ranking_items)}")
    if not ranking_items:
        print("⚠️ 데이터 없음")
    for idx, li in enumerate(ranking_items[:20], 1):
        a_tag = li.select_one('a[href^="/comic/"]')
        if not a_tag:
            continue
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
        # genre
        genre = ""
        genre_tag = a_tag.select_one(".txt-sub")
        if genre_tag:
            genre = genre_tag.text.strip()
        # author
        author = ""
        author_tag = a_tag.select_one(".txt-sub2")
        if author_tag:
            author = author_tag.text.strip()
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

# 크롤링 결과를 frontend/public 폴더로 자동 복사
try:
    shutil.copy("comico_ranking.json", "frontend/public/comico_ranking.json")
    print("✅ 최신 comico_ranking.json이 frontend/public 폴더로 복사되었습니다.")
except Exception as e:
    print(f"⚠️ public 폴더 복사 중 에러: {e}") 