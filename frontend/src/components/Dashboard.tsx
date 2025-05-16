import React, { useState, useEffect } from 'react';

interface RankingData {
  rank: number;
  title: string;
  author: string;
  genre: string;
  episode_count?: number;
  rating?: number;
  rating_count?: number;
  thumbnail: string;
  url: string;
  rank_change?: number;
  free_count?: number;
  like_count?: number;
  review_count?: number;
}

interface PlatformData {
  name: string;
  code: string;
  rankings: RankingData[];
}

const platformList: PlatformData[] = [
  { name: "メチャコミック", code: "mecha", rankings: [] },
  { name: "コミックシーモア", code: "cmoa", rankings: [] },
  { name: "レンタ", code: "renta", rankings: [] },
  { name: "トップトゥーンJP", code: "toptoon", rankings: [] },
  { name: "レジンJP", code: "lezhin", rankings: [] },
  { name: "DMM Books", code: "dmm", rankings: [] },
  { name: "コミコ", code: "comico", rankings: [] },
  { name: "漫画王国", code: "kmanga", rankings: [] },
  { name: "BookLive", code: "booklive", rankings: [] },
];

// 20위까지 샘플 데이터 생성
const sampleRankings: RankingData[] = Array.from({ length: 20 }, (_, i) => ({
  rank: i + 1,
  title: `샘플웹툰${i + 1}`,
  author: `작가${i + 1}`,
  genre: i % 2 === 0 ? '판타지' : '로맨스',
  episode_count: 100 - i,
  rating: 4.0 + ((20 - i) * 0.03),
  thumbnail: `https://placehold.co/120x160?text=${i + 1}`,
  url: '#',
  rank_change: i === 0 ? 0 : (i % 3 === 0 ? 1 : (i % 4 === 0 ? -2 : 0)),
  free_count: i % 2 === 0 ? 10 : undefined,
  like_count: i % 2 === 0 ? 50 : undefined,
  review_count: i % 2 === 0 ? 10 : undefined,
}));
platformList.forEach(p => { p.rankings = sampleRankings; });

const langText = {
  ko: {
    update: '업데이트',
    noPlatform: '선택된 플랫폼이 없습니다.',
    rank: '순위',
    thumbnail: '썸네일',
    title: '제목',
    author: '작가',
    genre: '장르',
    episode: '무료화수',
    episodeJa: '無料話数',
    authorJa: '作家',
    genreJa: 'ジャンル',
    rating: '별점',
    trend: '변동',
    view: '상세',
    togo: 'ToGo',
    lang: '한국어',
    langAlt: '日本語',
    platform: '플랫폼',
    all: '전체',
    date: '시작일',
    endDate: '종료일',
  },
  ja: {
    update: '更新',
    noPlatform: '選択されたプラットフォームがありません。',
    rank: '順位',
    thumbnail: 'サムネ',
    title: 'タイトル',
    author: '作家',
    genre: 'ジャンル',
    episode: '無料話数',
    episodeJa: '無料話数',
    authorJa: '作家',
    genreJa: 'ジャンル',
    rating: '評価',
    trend: '変動',
    view: '詳細',
    togo: 'ToGo',
    lang: '日本語',
    langAlt: '한국어',
    platform: 'プラットフォーム',
    all: '全て',
    date: '開始日',
    endDate: '終了日',
  }
};

// 문자열을 바이트 단위로 자르는 함수
function truncateByByte(str: string, maxBytes: number): string {
  let bytes = 0;
  let result = '';
  for (const ch of str) {
    const charCode = ch.charCodeAt(0);
    if (charCode <= 0x7f) bytes += 1; // 영문, 숫자
    else if (charCode <= 0x7ff) bytes += 2;
    else if (charCode <= 0xffff) bytes += 3;
    else bytes += 4;
    if (bytes > maxBytes) {
      result += '...';
      break;
    }
    result += ch;
  }
  return result;
}

const Dashboard: React.FC = () => {
  const [language, setLanguage] = useState<'ko' | 'ja'>('ko');
  const [startDate, setStartDate] = useState<string>(new Date().toISOString().slice(0, 10));
  const [endDate, setEndDate] = useState<string>(new Date().toISOString().slice(0, 10));
  const [selectedPlatform, setSelectedPlatform] = useState<string>('all');
  const [mechaData, setMechaData] = useState<RankingData[] | null>(null);
  const [cmoaData, setCmoaData] = useState<RankingData[] | null>(null);
  const [rentaData, setRentaData] = useState<RankingData[] | null>(null);
  const [lezhinData, setLezhinData] = useState<RankingData[] | null>(null);
  const [toptoonData, setToptoonData] = useState<RankingData[] | null>(null);
  const [dmmData, setDmmData] = useState<RankingData[] | null>(null);
  const [comicoData, setComicoData] = useState<RankingData[] | null>(null);
  const [kmangaData, setKmangaData] = useState<RankingData[] | null>(null);
  const [bookliveData, setBookliveData] = useState<RankingData[] | null>(null);
  const t = langText[language];

  useEffect(() => {
    if (selectedPlatform === 'mecha' || selectedPlatform === 'all') {
      fetch('/mecha_sample.json')
        .then(res => res.json())
        .then(data => setMechaData(data))
        .catch(() => setMechaData(null));
    }
    if (selectedPlatform === 'cmoa' || selectedPlatform === 'all') {
      fetch('/cmoa_sample.json')
        .then(res => res.json())
        .then(data => setCmoaData(data))
        .catch(() => setCmoaData(null));
    }
    if (selectedPlatform === 'renta' || selectedPlatform === 'all') {
      fetch('/renta_sample.json')
        .then(res => res.json())
        .then(data => setRentaData(data))
        .catch(() => setRentaData(null));
    }
    if (selectedPlatform === 'lezhin' || selectedPlatform === 'all') {
      fetch('/lezhin_sample.json')
        .then(res => res.json())
        .then(data => setLezhinData(
          data.map((item: RankingData, idx: number) => ({
            ...item,
            rank: idx + 1,
            author: item.author || '',
            url: item.url || '#',
          }))
        ))
        .catch(() => setLezhinData(null));
    }
    if (selectedPlatform === 'toptoon' || selectedPlatform === 'all') {
      fetch('/toptoon_sample.json')
        .then(res => res.json())
        .then(data => setToptoonData(
          data.map((item: RankingData, idx: number) => ({
            ...item,
            rank: idx + 1,
            url: item.url || '#',
          }))
        ))
        .catch(() => setToptoonData(null));
    }
    if (selectedPlatform === 'dmm' || selectedPlatform === 'all') {
      fetch('/dmm_sample.json')
        .then(res => res.json())
        .then(data => setDmmData(
          data.map((item: RankingData, idx: number) => ({
            ...item,
            rank: idx + 1,
            url: item.url || '#',
            genre: item.genre,
            rating: item.rating,
            rating_count: item.review_count,
          }))
        ))
        .catch(() => setDmmData(null));
    }
    if (selectedPlatform === 'comico' || selectedPlatform === 'all') {
      fetch('/comico_ranking.json')
        .then(res => res.json())
        .then(data => setComicoData(
          data.map((item: RankingData, idx: number) => ({
            ...item,
            rank: idx + 1,
            url: item.url || '#',
          }))
        ))
        .catch(() => setComicoData(null));
    }
    if (selectedPlatform === 'kmanga' || selectedPlatform === 'all') {
      fetch('/kmanga_ranking.json')
        .then(res => res.json())
        .then(data => setKmangaData(
          data.map((item: RankingData, idx: number) => ({
            ...item,
            rank: idx + 1,
            url: item.url || '#',
          }))
        ))
        .catch(() => setKmangaData(null));
    }
    if (selectedPlatform === 'booklive' || selectedPlatform === 'all') {
      fetch('/booklive_ranking.json')
        .then(res => res.json())
        .then(data => setBookliveData(
          data.map((item: RankingData, idx: number) => ({
            ...item,
            rank: idx + 1,
            url: item.url || '#',
          }))
        ))
        .catch(() => setBookliveData(null));
    }
  }, [selectedPlatform]);

  const handlePlatform = (code: string) => {
    setSelectedPlatform(code);
  };

  // platformList에서 mecha/cmoa/renta 등 실제 데이터로 대체
  const displayPlatformList = platformList.map(p => {
    if (p.code === 'mecha' && mechaData) return { ...p, rankings: mechaData };
    if (p.code === 'cmoa' && cmoaData) return { ...p, rankings: cmoaData };
    if (p.code === 'renta' && rentaData) return { ...p, rankings: rentaData };
    if (p.code === 'lezhin' && lezhinData) return { ...p, rankings: lezhinData };
    if (p.code === 'toptoon' && toptoonData) return { ...p, rankings: toptoonData };
    if (p.code === 'dmm' && dmmData) return { ...p, rankings: dmmData };
    if (p.code === 'comico' && comicoData) return { ...p, rankings: comicoData };
    if (p.code === 'kmanga' && kmangaData) return { ...p, rankings: kmangaData };
    if (p.code === 'booklive' && bookliveData) return { ...p, rankings: bookliveData };
    return p;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-6 flex flex-row-reverse items-center justify-between gap-4">
          <div className="flex flex-col md:flex-row md:items-center gap-2 md:gap-4 w-full justify-between">
            <div className="flex items-center gap-2">
              <label className="text-gray-700 font-medium text-sm">
                {t.date}
                <input
                  type="date"
                  value={startDate}
                  onChange={e => setStartDate(e.target.value)}
                  className="ml-1 border rounded px-2 py-1 text-sm focus:ring-primary-500 focus:border-primary-500"
                  style={{ minWidth: 120 }}
                />
              </label>
              <span className="mx-1 text-gray-400">~</span>
              <label className="text-gray-700 font-medium text-sm">
                {t.endDate}
                <input
                  type="date"
                  value={endDate}
                  onChange={e => setEndDate(e.target.value)}
                  className="ml-1 border rounded px-2 py-1 text-sm focus:ring-primary-500 focus:border-primary-500"
                  style={{ minWidth: 120 }}
                />
              </label>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setLanguage('ko')}
                className={`px-4 py-1 rounded border text-sm font-semibold transition ${language === 'ko' ? 'bg-primary-500 text-white border-primary-500' : 'bg-white text-primary-600 border-primary-200 hover:bg-primary-50'}`}
              >
                한국어
              </button>
              <button
                onClick={() => setLanguage('ja')}
                className={`px-4 py-1 rounded border text-sm font-semibold transition ${language === 'ja' ? 'bg-primary-500 text-white border-primary-500' : 'bg-white text-primary-600 border-primary-200 hover:bg-primary-50'}`}
              >
                日本語
              </button>
            </div>
          </div>
        </div>
      </div>
      <div className="flex justify-center mt-8 mb-10">
        <div className="flex flex-wrap gap-3 justify-center">
          <button
            onClick={() => handlePlatform('all')}
            className={`px-5 py-2 rounded-full border text-sm font-medium transition ${selectedPlatform === 'all' ? 'bg-primary-500 text-white border-primary-500 shadow' : 'bg-white text-primary-600 border-primary-200 hover:bg-primary-50'}`}
          >
            {t.all}
          </button>
          {platformList.map(platform => (
            <button
              key={platform.code}
              onClick={() => handlePlatform(platform.code)}
              className={`px-5 py-2 rounded-full border text-sm font-medium transition ${selectedPlatform === platform.code ? 'bg-primary-500 text-white border-primary-500 shadow' : 'bg-white text-primary-600 border-primary-200 hover:bg-primary-50'}`}
            >
              {platform.name}
            </button>
          ))}
        </div>
      </div>
      <div className="max-w-7xl mx-auto py-8 px-2 sm:px-6 lg:px-8">
        {selectedPlatform === 'all' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {displayPlatformList.map((platform) => (
              <div key={platform.name} className="bg-white rounded-xl shadow-md p-6 flex flex-col">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-bold text-gray-900">{platform.name}</h2>
                  <span className="text-xs text-gray-500">{t.update}: {endDate.replace(/-/g, '/')}</span>
                </div>
                {platform.rankings.slice(0, 5).map((item) => (
                  <div key={item.rank} className="flex bg-white rounded-xl shadow p-4 mb-4 gap-5 hover:shadow-lg transition min-h-[160px]">
                    <div className="relative flex-shrink-0">
                      <img src={item.thumbnail} alt={item.title} className="w-24 h-32 object-cover rounded-lg border" />
                    </div>
                    <div className="flex flex-col justify-between flex-1 min-w-0">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xl font-bold text-gray-900">{item.rank}位</span>
                          <span className="bg-green-100 text-green-700 text-xs font-bold rounded px-2 py-0.5">続話</span>
                        </div>
                        <div className="text-blue-600 font-bold text-lg leading-tight truncate max-w-[220px]">
                          <a href={item.url} target="_blank" rel="noopener noreferrer" className="hover:underline">{item.title}</a>
                        </div>
                        <div className="text-gray-700 text-sm font-semibold mt-1 mb-2">{truncateByByte(item.author, 25)}</div>
                        <div className="flex items-center gap-2 mb-2">
                          <span className="flex items-center gap-1 text-yellow-400 text-base">
                            {[...Array(5)].map((_, i) => (
                              <svg key={i} className={`w-4 h-4 ${item.rating && item.rating >= i + 1 ? '' : 'opacity-30'}`} fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.967a1 1 0 00.95.69h4.178c.969 0 1.371 1.24.588 1.81l-3.385 2.46a1 1 0 00-.364 1.118l1.287 3.966c.3.922-.755 1.688-1.54 1.118l-3.385-2.46a1 1 0 00-1.175 0l-3.385 2.46c-.784.57-1.838-.196-1.54-1.118l1.287-3.966a1 1 0 00-.364-1.118l-3.385-2.46c-.783-.57-.38-1.81.588-1.81h4.178a1 1 0 00.95-.69l1.286-3.967z" /></svg>
                            ))}
                          </span>
                          <span className="text-gray-900 font-bold text-base ml-1">{item.rating ? item.rating.toFixed(1) : '-'}</span>
                          <span className="text-blue-500 text-sm ml-1">({item.rating_count ?? item.like_count ?? item.review_count ?? '-'})</span>
                        </div>
                        <div className="flex flex-wrap gap-2 mt-1">
                          {item.genre.split(',').map((g, idx) => (
                            <span key={idx} className="bg-gray-100 text-gray-700 rounded px-2 py-0.5 text-xs border border-gray-200">{g.trim()}</span>
                          ))}
                        </div>
                      </div>
                      <div className="flex justify-end items-end mt-4 pt-2">
                        <a href={item.url} target="_blank" rel="noopener noreferrer" className="flex items-center justify-center px-4 py-1.5 bg-sky-400 text-white rounded-full text-sm font-semibold hover:bg-sky-500 transition min-w-[70px] min-h-[36px]">{t.togo}</a>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ))}
          </div>
        ) : (
          <div className="max-w-4xl mx-auto">
            {displayPlatformList
              .filter((p) => p.code === selectedPlatform)
              .map((platform) => (
                <div key={platform.name} className="bg-white rounded-xl shadow-md p-6 flex flex-col">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-bold text-gray-900">{platform.name}</h2>
                    <span className="text-xs text-gray-500">{t.update}: {endDate.replace(/-/g, '/')}</span>
                  </div>
                  {platform.rankings.slice(0, 20).map((item) => (
                    <div key={item.rank} className="flex bg-white rounded-xl shadow p-4 mb-4 items-center gap-4 hover:shadow-lg transition min-h-[120px]">
                      <div className="relative flex-shrink-0">
                        <img src={item.thumbnail} alt={item.title} className="w-20 h-28 object-cover rounded-lg border flex-shrink-0" />
                      </div>
                      <div className="flex-1 min-w-0 flex flex-col justify-center">
                        <div className="flex items-center justify-between gap-2">
                          <div className="text-primary-600 font-bold text-lg truncate">{item.rank}. <a href={item.url} target="_blank" rel="noopener noreferrer" className="hover:underline">{item.title}</a></div>
                        </div>
                        <div className="flex flex-wrap gap-4 mt-2 mb-1 text-sm">
                          <div className="flex items-center gap-1">
                            <span className="font-semibold text-purple-600">{t.authorJa}:</span>
                            <span className="text-gray-700">{truncateByByte(item.author, 25)}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <span className="font-semibold text-green-600">{t.genreJa}:</span>
                            <span className="text-gray-700">{item.genre}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <span className="font-semibold text-blue-600">{t.episodeJa}:</span>
                            <span className="text-gray-700">{item.episode_count ?? (typeof item.free_count === 'string' && item.free_count !== 'N/A' ? item.free_count : (typeof item.free_count === 'number' ? item.free_count : '-'))}</span>
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-2 items-center text-xs mt-1">
                          <span className="flex items-center text-yellow-500 font-semibold">
                            ★ {item.rating ? item.rating.toFixed(1) : '-'}
                            <span className="text-gray-400 text-xs ml-1">({item.rating_count ?? item.like_count ?? item.review_count ?? '-'})</span>
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center h-full">
                        <a href={item.url} target="_blank" rel="noopener noreferrer" className="flex items-center justify-center px-6 py-2 bg-sky-400 text-white rounded-full text-base font-semibold hover:bg-sky-500 transition min-w-[90px] min-h-[44px]">{t.togo}</a>
                      </div>
                    </div>
                  ))}
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard; 