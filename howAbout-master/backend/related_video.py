from pymongo import MongoClient
from datetime import datetime, timedelta


def fetch_most_related_videos_by_keyword(
    keyword: str,
    mongo_uri: str = "mongodb://localhost:27017/",
    db_name: str = "keyword",
    coll_name: str = "keyword",
    top_n: int = 5,
    days: int = 30,
):
    """
    최근 N일간의 동영상 중, 키워드 관련성 높은 동영상 Top-N 반환 (중복 제거)
    """
    client = MongoClient(mongo_uri)
    collection = client[db_name][coll_name]

    since = datetime.utcnow() - timedelta(days=days)

    query = {
        f"combined_score.{keyword}": { "$exists": True },
        "timestamp": { "$gte": since }
    }

    projection = {
        "_id": 0,
        "video_id": 1,
        "title": 1,
        "timestamp": 1,
        f"combined_score.{keyword}": 1
    }

    docs = list(collection.find(query, projection))

    # video_id 기준으로 중복 제거하며 가장 높은 score만 유지
    video_map = {}
    for doc in docs:
        vid = doc["video_id"]
        score = doc["combined_score"][keyword]
        if vid not in video_map or score > video_map[vid]["score"]:
            video_map[vid] = {
                "video_id": vid,
                "title": doc.get("title", ""),
                "score": score,
                "timestamp": doc.get("timestamp")
            }

    # score 기준 정렬 후 top_n 추출
    sorted_videos = sorted(video_map.values(), key=lambda x: -x["score"])

    return sorted_videos[:top_n]

