# Wisebirds Webtoon Research

일본 웹툰 플랫폼 10곳의 일일 랭킹 Top 20을 자동으로 수집하고 통합하여 보여주는 리서치 대시보드입니다.

## 주요 기능

- 10개 일본 웹툰 플랫폼의 일일 랭킹 Top 20 자동 수집
- 매일 오전 8시 정각에 자동 수집
- 플랫폼별 1위 작품 카드 형태 강조 표시
- 작품별 상세 정보 제공 (제목, 작가, 장르, 화수, 별점 등)
- 랭킹 변화 추이 시각화
- 한국어/일본어 2개 언어 지원

## 설치 방법

1. Python 3.8 이상 설치
2. 프로젝트 클론
```bash
git clone [repository-url]
cd wisebirds-webtoon-research
```

3. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

4. 의존성 설치
```bash
pip install -r requirements.txt
```

## 실행 방법

1. 크롤러 실행
```bash
python src/main.py
```

2. 웹 대시보드 실행 (개발 중)
```bash
# 추후 추가 예정
```

## 프로젝트 구조

```
wisebirds-webtoon-research/
├── src/
│   ├── crawlers/           # 각 사이트별 크롤러 모듈
│   ├── utils/             # 공통 유틸리티 함수
│   └── config/            # 설정 파일
├── frontend/              # React 기반 프론트엔드
├── requirements.txt       # Python 의존성
└── README.md             # 프로젝트 문서
```

## 크롤링 대상 사이트

1. メチャコミック (Mecha Comic)
2. コミックシーモア (Comic Seymour)
3. レンタ (Renta)
4. トップトゥーンJP (Toptoon JP)
5. レジンJP (Lezhin JP)
6. DMM Books
7. コミコ (Comico)
8. マガポケ (Maga Pocket)
9. 漫画王国 (Manga Kingdom)
10. BookLive

## 주의사항

- 각 사이트의 이용약관을 준수하여 크롤링을 수행합니다.
- 적절한 딜레이를 두어 서버에 부담을 주지 않도록 합니다.
- User-Agent 헤더를 포함하여 정상적인 접근임을 표시합니다.

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 