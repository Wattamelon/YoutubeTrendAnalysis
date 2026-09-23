import json  
from pymongo import MongoClient
from datetime import datetime, timedelta

# 🔹 입력: 분석하고 싶은 키워드
import sys
TARGET_KEYWORD = sys.argv[1]


# 🔹 기간 설정: 최근 60일
today = datetime.now().date()
date_threshold = today - timedelta(days=60)

# 🔹 MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["keyword"]
collection = db["keyword"]

# 🔹 결과 누적용 딕셔너리
daily_data = {}

# 🔹 MongoDB 문서 순회
for doc in collection.find({}, {
    "combined_score": 1,
    "view_count": 1,
    "subscriber_count": 1,
    "timestamp": 1
}):
    combined_score = doc.get("combined_score", {})
    view_count = doc.get("view_count", 0)
    subscriber_count = doc.get("subscriber_count", 0)
    timestamp = doc.get("timestamp")

    if not timestamp or TARGET_KEYWORD not in combined_score:
        continue

    date_key = datetime.fromisoformat(str(timestamp)).date()
    if date_key < date_threshold:
        continue

    date_str = date_key.isoformat()
    if date_str not in daily_data:
        daily_data[date_str] = {"total_view": 0, "total_subs": 0}

    daily_data[date_str]["total_view"] += view_count
    daily_data[date_str]["total_subs"] += subscriber_count

# 🔹 결과 정리 및 출력
results = []
for date, stats in sorted(daily_data.items()):
    view = stats["total_view"]
    subs = stats["total_subs"]
    growth_score = view / subs if subs else 0
    results.append({
        "keyword": TARGET_KEYWORD,
        "date": date,
        "total_view": view,
        "total_subs": subs,
        "growth_score": round(growth_score, 5)
    })


# 🔹 터미널에 출력 (이건 디버깅용이므로 지워도 무방)
# print(f"\n📈 키워드 '{TARGET_KEYWORD}'의 최근 60일 성장 점수:\n")
# for item in results:
#     print(f"{item['date']} | 조회수: {item['total_view']} | 구독자수: {item['total_subs']} | 성장점수: {item['growth_score']}")

# 🔹 최종 결과 JSON으로 출력 (Node.js에서 파싱 가능하게!)
print(json.dumps(results, ensure_ascii=False))