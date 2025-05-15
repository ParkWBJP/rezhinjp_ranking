import requests
from bs4 import BeautifulSoup
import json
import os
import re

BASE_URL = "https://www.lezhin.jp"
RANKING_URL = f"{BASE_URL}/ja/ranking?genre=_all&rankType=realtime&filter=all"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_page_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_background_image(style):
    # style 예시: background-image:url('https://...');
    match = re.search(r"background-image:\s*url\(['\"]?(.*?)['\"]?\)", style)
    if match:
        return match.group(1)
    return "N/A"

def parse_ranking_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    comics_data = []
    # 각 웹툰 항목: li.rankingItem__v6hpm
    cards = soup.find_all('li', class_='rankingItem__v6hpm')
    for card in cards[:20]:
        # 제목
        title_tag = card.select_one('div[class^="rankingItem__title__"] > span[class^="rankingItem__lineClamp__"]')
        title = title_tag.text.strip() if title_tag else "N/A"
        # 썸네일: img 태그의 src만 추출
        thumb_div = card.select_one('div[class^="rankingItem__thumb__"]')
        thumbnail = "N/A"
        if thumb_div:
            img_tag = thumb_div.find('img')
            if img_tag and img_tag.has_attr('src'):
                thumbnail = img_tag['src']
        if not thumbnail or thumbnail == "N/A":
            thumbnail = "https://placehold.co/120x160?text=No+Image"
        # 랜딩 URL
        link_tag = card.select_one('a[class^="rankingItem__link__"]')
        landing_url = BASE_URL + link_tag['href'] if link_tag and link_tag.has_attr('href') else "N/A"
        # 장르
        genre_tag = card.select_one('span[class^="rankingItem__genre__"]')
        genre = genre_tag.text.strip() if genre_tag else "N/A"
        # 작가
        artist_tag = card.select_one('span[class^="rankingItem__artist__"]')
        artist = artist_tag.text.strip() if artist_tag else "N/A"
        # 무료화수
        free_tag = card.select_one('div.rankingItem__free__SI8Cc')
        free_count = free_tag.text.strip() if free_tag else "N/A"
        comics_data.append({
            "title": title,
            "thumbnail": thumbnail,
            "landing_url": landing_url,
            "artist": artist,
            "genre": genre,
            "free_count": free_count,
            "platform": "Lezhin"
        })
    return comics_data

def save_to_json(data, filename="frontend/public/lezhin_sample.json"):
    output_dir = os.path.dirname(filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    print("레진 랭킹 페이지 크롤링 중...")
    html_content = fetch_page_content(RANKING_URL)
    if html_content:
        comics = parse_ranking_page(html_content)
        save_to_json(comics)
        print(f"Successfully fetched and saved data for {len(comics)} comics.")
    else:
        print("Failed to fetch ranking page content.") 