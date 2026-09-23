"""import json
from pymongo import MongoClient
from collections import defaultdict
from datetime import datetime, timezone

def run_ranking(start_date, end_date):
    # ✅ JSON 외 출력 제거 (Node.js에서는 JSON만 받아야 하니까!)
    # print(f"조회 구간: {start_date} ~ {end_date}", flush=True)

    client = MongoClient("mongodb://localhost:27017/")
    collection = client["keyword"]["keyword"]

    alpha = 0.5
    skipped = 0
    scores = defaultdict(lambda: defaultdict(float))
    counts = defaultdict(lambda: defaultdict(int))

    query = {
        "timestamp": {"$gte": start_date, "$lt": end_date}
    }
    # count = collection.count_documents(query)
    # print(f"해당 구간 문서 수: {count}", flush=True)

    for doc in collection.find(query):
        try:
            category = doc.get("category")
            view_count = doc.get("view_count", 0)
            published_str = doc.get("published_at")
            timestamp = doc.get("timestamp")
            combined_score = doc.get("combined_score", {})

            if not (category and published_str and timestamp and combined_score):
                # print(f"누락 필드 있음 → {doc.get('_id')}")
                skipped += 1
                continue

            published_at = datetime.fromisoformat(published_str)
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)

            hours = (timestamp - published_at).total_seconds() / 3600
            if hours <= 0:
                skipped += 1
                continue

            view_speed = view_count / hours

            for keyword, score in combined_score.items():
                scores[category][keyword] += view_speed * score
                counts[category][keyword] += 1

        except Exception:
            skipped += 1

    result = {}
    for category in scores:
        keyword_list = []
        for keyword in scores[category]:
            total = scores[category][keyword]
            count = counts[category][keyword]
            adjusted = total / (count ** alpha)
            keyword_list.append({"keyword": keyword, "score": round(adjusted, 2)})
        keyword_list.sort(key=lambda x: x["score"], reverse=True)
        result[category] = keyword_list[:50]

    # ✅ JSON만 출력
    return result 


from datetime import datetime, timedelta
import os, json

def find_closest_date(target_days_ago: int, folder="rankings"):
    target = datetime.now().date() - timedelta(days=target_days_ago)
    available = [f for f in os.listdir(folder) if f.endswith(".json")]
    available_dates = [datetime.strptime(f.split(".")[0], "%Y-%m-%d").date() for f in available]
    if not available_dates:
        return None
    closest = min(available_dates, key=lambda d: abs((d - target).days))
    return f"{folder}/{closest}.json"

def load_ranking(filepath):
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

def compare_rankings(current: dict, past: dict, top_k=30):
    comparison = {}
    for category in current:
        cur_rank = {k["keyword"]: i for i, k in enumerate(current[category][:top_k], 1)}
        past_rank = {k["keyword"]: i for i, k in enumerate(past.get(category, [])[:top_k], 1)}
        keywords = set(cur_rank.keys()).union(past_rank.keys())
        result = []
        for kw in keywords:
            now = cur_rank.get(kw)
            old = past_rank.get(kw)
            if now and old:
                change = old - now
                movement = "상승" if change > 0 else "하락" if change < 0 else "유지"
            elif now:
                change, movement = None, "신규 진입"
            else:
                change, movement = None, "랭크 아웃"
            result.append({
                "keyword": kw,
                "current_rank": now,
                "previous_rank": old,
                "movement": movement,
                "rank_change": change
            })
        comparison[category] = sorted(result, key=lambda x: x["current_rank"] if x["current_rank"] else 999)
    return comparison
"""


from pymongo import MongoClient
from datetime import datetime, timedelta
from collections import defaultdict

# === MongoDB 연결 ===
client = MongoClient("mongodb://localhost:27017")
db = client["keyword"]
collection = db["keyword"]

# === 1. 주어진 기간 내 키워드 랭킹 계산 (카테고리별) ===
def run_ranking_by_category(start, end):
    docs = list(collection.find({
        "timestamp": {"$gte": start, "$lt": end}
    }, {"combined_score": 1, "category": 1}))

    category_rankings = defaultdict(lambda: defaultdict(float))

    for doc in docs:
        cat = doc.get("category")
        scores = doc.get("combined_score", {})
        for kw, score in scores.items():
            category_rankings[cat][kw] += score

    result = {}
    for cat, kw_scores in category_rankings.items():
        sorted_keywords = sorted(kw_scores.items(), key=lambda x: x[1], reverse=True)
        result[cat] = [
            {"keyword": kw, "score": round(score, 3)} for kw, score in sorted_keywords
        ]

    return result

# === 2. 시작일, 종료일 계산 ===
def get_period_range(period):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if period == "today":
        return today, today + timedelta(days=1), 1
    elif period == "week":
        return today - timedelta(days=6), today + timedelta(days=1), 7
    elif period == "month":
        return today - timedelta(days=29), today + timedelta(days=1), 30
    else:
        raise ValueError("지원하지 않는 기간입니다.")

# === 3. 과거 날짜 중 가장 가까운 날짜 찾기 ===
def find_closest_date(start, window_days):
    lower_bound = start - timedelta(days=15)
    upper_bound = start - timedelta(days=1)
    timestamps = collection.distinct("timestamp", {"timestamp": {"$gte": lower_bound, "$lt": upper_bound}})
    dates = sorted({ts.date() for ts in timestamps})
    target = (start - timedelta(days=window_days)).date()
    return min(dates, key=lambda d: abs((d - target).days)) if dates else None

# === 4. 현재 vs 과거 랭킹 비교 ===
def compare_rankings_by_category(current, past, top_k=30):
    results = {}
    for category in current:
        cur_rank = {item["keyword"]: i for i, item in enumerate(current.get(category, [])[:top_k], 1)}
        past_rank = {item["keyword"]: i for i, item in enumerate(past.get(category, [])[:top_k], 1)}
        all_keywords = set(cur_rank) | set(past_rank)

        cat_result = []
        for kw in all_keywords:
            cur_pos = cur_rank.get(kw)
            past_pos = past_rank.get(kw)
            if cur_pos and past_pos:
                diff = past_pos - cur_pos
                movement = "상승" if diff > 0 else "하락" if diff < 0 else "유지"
            elif cur_pos:
                diff, movement = None, "신규 진입"
            else:
                diff, movement = None, "랭크 아웃"
            cat_result.append({
                "keyword": kw,
                "current_rank": cur_pos,
                "previous_rank": past_pos,
                "movement": movement,
                "rank_change": diff
            })

        results[category] = sorted(cat_result, key=lambda x: x["current_rank"] if x["current_rank"] else 999)
    return results

 