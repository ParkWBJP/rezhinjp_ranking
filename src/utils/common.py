import logging
from datetime import datetime
from typing import Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_headers() -> Dict[str, str]:
    """기본 User-Agent 헤더를 반환합니다."""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
    }

def get_soup(url: str) -> Optional[BeautifulSoup]:
    """URL에서 BeautifulSoup 객체를 생성합니다."""
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        logger.error(f"Error fetching {url}: {str(e)}")
        return None

def get_selenium_driver() -> webdriver.Chrome:
    """Selenium WebDriver를 설정하고 반환합니다."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'user-agent={get_headers()["User-Agent"]}')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def validate_ranking_data(data: Dict[str, Any], platform: str) -> bool:
    """수집된 랭킹 데이터의 유효성을 검사합니다."""
    required_fields = ['rank', 'title', 'author', 'genre', 'thumbnail', 'url']
    
    if not all(field in data for field in required_fields):
        logger.error(f"Missing required fields in {platform} data: {data}")
        return False
    
    if not isinstance(data['rank'], int) or data['rank'] < 1 or data['rank'] > 20:
        logger.error(f"Invalid rank value in {platform} data: {data['rank']}")
        return False
    
    return True

def format_ranking_data(
    rank: int,
    title: str,
    author: str,
    genre: str,
    thumbnail: str,
    url: str,
    episode_count: Optional[int] = None,
    rating: Optional[float] = None
) -> Dict[str, Any]:
    """랭킹 데이터를 표준 형식으로 변환합니다."""
    return {
        'rank': rank,
        'title': title,
        'author': author,
        'genre': genre,
        'episode_count': episode_count,
        'rating': rating,
        'thumbnail': thumbnail,
        'url': url,
        'crawled_at': datetime.now().isoformat()
    } 