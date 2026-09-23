# ✅ category_keywords 컬렉션을 기반으로 특정 키워드에 대한 통계 계산 (최신 날짜 기준)
# 입력: python graded_keywords.py 키워드
# 출력: JSON (조회수, 선호도, 참여도, 성장성, 등급 등)

import json
import sys
from collections import defaultdict
import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

# === [1] 파라미터 입력 ===
if len(sys.argv) != 2:
    print(json.dumps({"error": "❌ 키워드를 인자로 전달해주세요"}))
    sys.exit(1)

target_keyword = sys.argv[1]

# === [2] MongoDB 연결 ===
client = MongoClient("mongodb://localhost:27017")
video_col = client["keyword"]["keyword"]
category_col = client["test_database"]["category_keywords"]

# === [3] 해당 키워드의 카테고리 찾기 ===
category = None
for doc in category_col.find():
    for item in doc.get("ranked_keywords", []):
        if item.get("키워드") == target_keyword:
            category = doc.get("category")
            break
    if category:
        break

if not category:
    print(json.dumps({"error": "❌ 해당 키워드는 어떤 카테고리에도 속해있지 않습니다."}))
    sys.exit(1)

# === [4] 가장 최신 timestamp 추출 ===
latest_doc = video_col.find({"timestamp": {"$exists": True}}, {"timestamp": 1}).sort("timestamp", -1).limit(1)
latest_timestamp = None
for doc in latest_doc:
    latest_timestamp = datetime.fromisoformat(str(doc["timestamp"])).date()

# === [5] 영상 통계 누적 ===
stats = {
    "view_count": 0,
    "like_count": 0,
    "comment_count": 0,
    "subscriber_weighted_view": 0,
    "total_subscribers": 0
}

all_docs = video_col.find({}, {
    "view_count": 1,
    "like_count": 1,
    "comment_count": 1,
    "subscriber_count": 1,
    "combined_score": 1,
    "timestamp": 1
})

for doc in all_docs:
    if "timestamp" not in doc or datetime.fromisoformat(str(doc["timestamp"])).date() != latest_timestamp:
        continue

    view = doc.get("view_count", 0)
    like = doc.get("like_count", 0)
    comment = doc.get("comment_count", 0)
    subscribers = doc.get("subscriber_count", 0)
    combined_score = doc.get("combined_score", {})

    if target_keyword not in combined_score:
        continue

    stats["view_count"] += view
    stats["like_count"] += like
    stats["comment_count"] += comment
    if subscribers > 0:
        stats["subscriber_weighted_view"] += view
        stats["total_subscribers"] += subscribers

# === [6] 계산 ===
view = stats["view_count"]
like = stats["like_count"]
comment = stats["comment_count"]
subs = stats["total_subscribers"]
weighted_view = stats["subscriber_weighted_view"]

preference = like / view if view else 0
engagement = comment / view if view else 0
growth = (weighted_view / subs) if subs else 0

# === [7] 정규화 및 등급 ===
df = pd.DataFrame([{"preference": preference, "engagement": engagement}])
scaler = MinMaxScaler()
df[["normalized_preference", "normalized_engagement"]] = scaler.fit_transform(df[["preference", "engagement"]])

pref_quart = np.percentile(df["preference"], [25, 50, 75])
eng_quart = np.percentile(df["engagement"], [25, 50, 75])

def assign_grade(value, quartiles):
    if value <= quartiles[0]: return "D"
    elif value <= quartiles[1]: return "C"
    elif value <= quartiles[2]: return "B"
    else: return "A"

# === [8] 출력 ===
result = {
    "view_count": int(view),
    "like_count": int(like),
    "comment_count": int(comment),
    "preference": round(preference, 5),
    "engagement": round(engagement, 5),
    "growth_score": round(growth, 5),
    "normalized_preference": round(df.iloc[0]["normalized_preference"], 5),
    "normalized_engagement": round(df.iloc[0]["normalized_engagement"], 5),
    "preference_grade": assign_grade(preference, pref_quart),
    "engagement_grade": assign_grade(engagement, eng_quart)
}

print(json.dumps(result, ensure_ascii=False, indent=2))
sys.stdout.flush()
