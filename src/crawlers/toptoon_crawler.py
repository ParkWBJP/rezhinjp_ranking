from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import os
import time

# 기본 URL
BASE_URL = "https://toptoon.jp"
RANKING_URL = f"{BASE_URL}/daily"

# Selenium 브라우저 옵션 설정 (화면 안 띄우는 headless 모드)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')

def fetch_ranking_data():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(RANKING_URL)
    time.sleep(2)  # 페이지 렌더링 대기
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    comics_data = []
    all_a_tags = soup.find_all('a', href=True)
    for item in all_a_tags:
        href = item['href']
        if href.startswith('/content/'):
            img_tag = item.find('img')
            # 썸네일: src 우선, 없으면 data-src
            thumbnail_url = "N/A"
            if img_tag:
                if img_tag.has_attr('src') and img_tag['src']:
                    thumbnail_url = img_tag['src']
                elif img_tag.has_attr('data-src'):
                    thumbnail_url = img_tag['data-src']
                if thumbnail_url.startswith('/'):
                    thumbnail_url = BASE_URL + thumbnail_url
            # 제목: img의 alt
            title = img_tag['alt'] if img_tag and 'alt' in img_tag.attrs else "N/A"
            # 상세페이지 URL
            landing_url = BASE_URL + href
            comics_data.append({
                "title": title,
                "thumbnail": thumbnail_url,
                "landing_url": landing_url
            })
            if len(comics_data) >= 20:
                break
    driver.quit()
    return comics_data

def fetch_detail_data(comic):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(comic['landing_url'])
    time.sleep(1.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # 작가 정보
    author_blocks = soup.select('div.flex.items-center.gap-x-\[2px\].leading-120.tracking-primary')
    authors = []
    for block in author_blocks:
        author = block.select_one('a')
        if author:
            authors.append(author.text.strip())
    author_str = ' / '.join(authors) if authors else "N/A"
    # 장르 정보 (예시: 장르가 있는 span이나 div, 실제 구조에 맞게 수정 필요)
    genre = "N/A"
    genre_tag = soup.find('span', class_='text-epilistComicInfoGenreText')
    if genre_tag:
        genre = genre_tag.text.strip()
    # 별점(3.0 고정)
    rating = 3.0
    # 별점 참여수(좋아요 수)
    rating_count = "N/A"
    like_img = soup.find('img', {'alt': '', 'src': '/images/common/badge/icon_thumbsup_active_red.png'})
    if like_img:
        like_span = like_img.find_next('span')
        if like_span:
            rating_count = like_span.text.strip()
    driver.quit()
    return author_str, genre, rating, rating_count

def save_to_json(data, filename="frontend/public/toptoon_sample.json"):
    """수집된 데이터를 JSON 파일로 저장합니다."""
    # frontend/public 폴더가 없으면 생성
    output_dir = os.path.dirname(filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    print("Selenium으로 TopToon 랭킹 페이지 접속 중...")
    comics = fetch_ranking_data()
    print(f"Found {len(comics)} comics. 상세페이지 정보 수집 중...")
    for comic in comics:
        author, genre, rating, rating_count = fetch_detail_data(comic)
        comic['author'] = author
        comic['genre'] = genre
        comic['rating'] = rating
        comic['rating_count'] = rating_count
        time.sleep(0.5)
    save_to_json(comics)
    print(f"Successfully fetched and saved data for {len(comics)} comics.") 