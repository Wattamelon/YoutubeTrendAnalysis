import json
from pymongo import MongoClient
from collections import defaultdict
from datetime import datetime
import sys

def run_ranking(start_date, end_date):

    #print(f"📆 조회 구간: {start_date} ~ {end_date}",file=sys.stderr)
    
    client = MongoClient("mongodb://localhost:27017/")
    collection = client["keyword"]["keyword"]

    alpha = 0.5
    skipped = 0
    scores = defaultdict(lambda: defaultdict(float))
    counts = defaultdict(lambda: defaultdict(int))

    query = {
        "timestamp": {"$gte": start_date, "$lt": end_date}
    }
    count = collection.count_documents(query)
    #print(f"🔍 해당 구간 문서 수: {count}", flush=True)

    for doc in collection.find(query):
        try:
            category = doc.get("category")
            view_count = doc.get("view_count", 0)
            published_str = doc.get("published_at")
            timestamp = doc.get("timestamp")
            combined_score = doc.get("combined_score", {})
            

            # 👉 여기 로그 추가
            if not (category and published_str and timestamp and combined_score):
                print(f"⚠️ 누락 필드 있음 → {doc.get('_id')}",file=sys.stderr)
                skipped += 1
                continue

            published_at = datetime.fromisoformat(published_str)
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)
            if timestamp.tzinfo is None:
                from datetime import timezone
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

    print(json.dumps(result, ensure_ascii=False))  # stdout으로 출력
