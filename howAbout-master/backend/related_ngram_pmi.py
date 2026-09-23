# pip install pymongo python-dateutil
from pymongo import MongoClient
from collections import Counter
from math import log
from datetime import datetime, timedelta
from typing import List, Tuple

def ngrams(seq: List[str], n: int) -> List[Tuple[str, ...]]:
    return [tuple(seq[i:i+n]) for i in range(len(seq) - n + 1)]

def related_keyword_video_level(
    keyword: str,
    mongo_uri: str = "mongodb://localhost:27017/",
    db: str = "tokenize",
    coll: str = "tokenize",
    n: int = 5,
    min_co: int = 2,
    top_n: int = 20,
    days: int = 30,                       # ✨ 최근 N일만 분석 (default 7)
) -> List[str]:
    client = MongoClient(mongo_uri)
    collection = client[db][coll]

    since = datetime.utcnow() - timedelta(days=days)

    # ── ① 영상 단위 통계 누적 ───────────────────────────────
    total_videos   = 0
    vids_with_kw   = 0
    freq_word      = Counter()
    co_counter     = Counter()

    cursor = collection.find(
        {"timestamp": {"$gte": since}},
        {"comments_noun_list": 1, "_id": 0}
    )

    for doc in cursor:
        total_videos += 1
        tokens = [tok for c in doc["comments_noun_list"] for tok in c]
        if len(tokens) < n:
            continue

        seen_words, seen_co = set(), set()
        has_kw = False

        for gram in ngrams(tokens, n):
            if keyword in gram:
                has_kw = True
                seen_co.update([w for w in gram if w != keyword])
            seen_words.update(gram)

        for w in seen_words:
            if w != keyword:
                freq_word[w] += 1
        for w in seen_co:
            co_counter[w] += 1
        if has_kw:
            vids_with_kw += 1

    if vids_with_kw == 0:
        return []

    # ── ② PMI × 빈도 스코어 계산 ──────────────────────────
    p_kw = vids_with_kw / total_videos
    scored = []
    for w, c_xy in co_counter.items():
        if c_xy < min_co:
            continue
        p_w  = freq_word[w] / total_videos
        p_xy = c_xy / total_videos
        pmi  = log((p_xy / (p_kw * p_w)) + 1e-12)
        scored.append((w, pmi * c_xy))   # 결합강도 * 빈도

    scored.sort(key=lambda x: -x[1])
    return [w for w, _ in scored[:top_n]]
