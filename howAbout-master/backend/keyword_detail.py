
import json
from collections import defaultdict
from pymongo import MongoClient
from datetime import datetime
import numpy as np


def analyze_keyword_success(target_keyword: str):
    mongo_uri = "mongodb://localhost:27017"
    client = MongoClient(mongo_uri)
    db = client["keyword"]
    collection = db["keyword"]

    # 최신 날짜 가져오기
    latest_doc = collection.find(
        {"timestamp": {"$exists": True}}, {"timestamp": 1}
    ).sort("timestamp", -1).limit(1)
    latest_timestamp = None
    for doc in latest_doc:
        latest_timestamp = datetime.fromisoformat(str(doc["timestamp"])).date()

    # 통계 누적용 변수
    view_total = 0
    like_total = 0
    comment_total = 0
    weighted_view_total = 0
    subscriber_total = 0

    # 최신 날짜에 해당하는 문서에서 keyword 포함된 것만 수집
    all_docs = list(collection.find({
        "timestamp": {"$gte": datetime.combine(latest_timestamp, datetime.min.time())}
    }))

    for doc in all_docs:
        combined_score = doc.get("combined_score", {})
        if target_keyword not in combined_score:
            continue

        view = doc.get("view_count", 0)
        like = doc.get("like_count", 0)
        comment = doc.get("comment_count", 0)
        subscriber = doc.get("subscriber_count", 0)

        view_total += view
        like_total += like
        comment_total += comment
        if subscriber > 0:
            weighted_view_total += view
            subscriber_total += subscriber

    if view_total == 0:
        return json.dumps({"error": f"'{target_keyword}' 키워드는 최신 날짜 데이터에 존재하지 않습니다."}, ensure_ascii=False, indent=2)

    preference = like_total / view_total
    engagement = comment_total / view_total
    growth_score = (weighted_view_total / subscriber_total) if subscriber_total else 0

    # 등급 분포 기준값 설정 (운영자 기준 조정 가능)
    def assign_grade(value, q1, q2, q3):
        if value <= q1: return "D"
        elif value <= q2: return "C"
        elif value <= q3: return "B"
        else: return "A"

    # 기준 사분위수 (수동 설정)
    pref_quartiles = [0.05, 0.10, 0.20]
    eng_quartiles = [0.01, 0.03, 0.05]

    result = {
        "view_count": view_total,
        "like_count": like_total,
        "comment_count": comment_total,
        "growth_score": round(growth_score, 5),
        "preference_grade": assign_grade(preference, *pref_quartiles),
        "engagement_grade": assign_grade(engagement, *eng_quartiles)
    }

    return json.dumps(result, ensure_ascii=False, indent=2)

