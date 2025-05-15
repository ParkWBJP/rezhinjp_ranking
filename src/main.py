import logging
import schedule
import time
from datetime import datetime
from typing import Dict, List, Any
from crawlers.mecha import MechaCrawler
# 다른 크롤러들도 여기에 import 예정

logger = logging.getLogger(__name__)

class WebtoonRankingCollector:
    """웹툰 랭킹 수집기"""
    
    def __init__(self):
        self.crawlers = {
            'mecha': MechaCrawler(),
            # 다른 크롤러들도 여기에 추가 예정
        }
    
    def collect_all_rankings(self) -> Dict[str, List[Dict[str, Any]]]:
        """모든 플랫폼의 랭킹을 수집합니다."""
        all_rankings = {}
        
        for platform, crawler in self.crawlers.items():
            try:
                logger.info(f"Collecting rankings from {platform}")
                rankings = crawler.get_rankings()
                
                if rankings:
                    all_rankings[platform] = rankings
                    logger.info(f"Successfully collected {len(rankings)} rankings from {platform}")
                else:
                    logger.warning(f"No rankings collected from {platform}")
                    
            except Exception as e:
                logger.error(f"Error collecting rankings from {platform}: {str(e)}")
                continue
        
        return all_rankings
    
    def save_rankings(self, rankings: Dict[str, List[Dict[str, Any]]]):
        """수집된 랭킹을 저장합니다. (Firebase 연동 전 임시 저장)"""
        # TODO: Firebase 연동 후 구현
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        logger.info(f"Rankings collected at {timestamp}")
        # 임시로 로그만 출력
        for platform, platform_rankings in rankings.items():
            logger.info(f"{platform}: {len(platform_rankings)} rankings")
    
    def run_collection(self):
        """랭킹 수집을 실행합니다."""
        logger.info("Starting ranking collection")
        rankings = self.collect_all_rankings()
        self.save_rankings(rankings)
        logger.info("Ranking collection completed")

def main():
    """메인 실행 함수"""
    collector = WebtoonRankingCollector()
    
    # 매일 오전 8시에 실행되도록 스케줄링
    schedule.every().day.at("08:00").do(collector.run_collection)
    
    # 테스트를 위해 즉시 한 번 실행
    collector.run_collection()
    
    # 스케줄러 실행
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 