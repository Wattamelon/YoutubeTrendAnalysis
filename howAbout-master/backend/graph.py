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
            "video_id": 1,
            f"combined_score.{keyword}": 1,
            "_id": 0
        }
    )

    # ✅ 날짜별 video_id 중복 제거 후 가장 높은 점수만 유지
    daily_video_map = {}  # {date: {video_id: score}}

    for doc in cursor:
        timestamp = doc.get("timestamp")
        video_id = doc.get("video_id")
        if not timestamp or not video_id:
            continue
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        date_str = timestamp.strftime("%Y-%m-%d")
        score = doc["combined_score"][keyword]

        if date_str not in daily_video_map:
            daily_video_map[date_str] = {}

        existing_score = daily_video_map[date_str].get(video_id, 0)
        if score > existing_score:
            daily_video_map[date_str][video_id] = score

    # ✅ 날짜별 점수 합산 → 정규화
    date_score_map = {
        date: sum(videos.values()) for date, videos in daily_video_map.items()
    }

    # ✅ 정규화 (최대값 기준)
    max_score = max(date_score_map.values()) if date_score_map else 1

    trend = [
        {"date": date, "score": round(score / max_score, 5)}
        for date, score in sorted(date_score_map.items())
    ]
    return trend


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ 키워드를 인자로 전달해주세요", file=sys.stderr)
        sys.exit(1)

    keyword = sys.argv[1]
    trend_data = get_keyword_trend_series(keyword)
    print(json.dumps(trend_data, ensure_ascii=False))
