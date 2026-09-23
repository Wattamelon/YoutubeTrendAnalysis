import sys
import json
from pymongo import MongoClient
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

def get_keyword_trend_series(keyword: str):
    client = MongoClient("mongodb://localhost:27017/")
    coll = client["keyword"]["keyword"]

    # 키워드가 포함된 모든 문서 가져오기 (날짜 제한 없음)
    cursor = coll.find(
        {
            f"combined_score.{keyword}": { "$exists": True }
        },
        {
            "timestamp": 1,
            f"combined_score.{keyword}": 1,
            "_id": 0
        }
    )

    date_score_map = {}

    for doc in cursor:
        timestamp = doc.get("timestamp")
        if not timestamp:
            continue
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        date_str = timestamp.strftime("%Y-%m-%d")
        score = doc["combined_score"][keyword]
        date_score_map[date_str] = date_score_map.get(date_str, 0) + score

    # 날짜순 정렬된 리스트로 변환
    trend = [{"date": k, "score": round(v, 2)} for k, v in sorted(date_score_map.items())]
    return trend


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ 키워드를 인자로 전달해주세요", file=sys.stderr)
        sys.exit(1)

    keyword = sys.argv[1]
    trend_data = get_keyword_trend_series(keyword)
    print(json.dumps(trend_data, ensure_ascii=False))
