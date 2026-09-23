from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from fetch_video import *

client = MongoClient("mongodb://localhost:27017")

CATEGORIES = {
    "News & Politics": "25",
    'Music' : "10",
    'Sports' : "17",
    'Gaming' : "20",
    'Science & Technology': "28"
}


def get_utc_range_from_kst_date(kst_date_str):
    """
    KST 기준 날짜 문자열을 받아, UTC 기준 시작/종료 시간 범위를 반환

    예: '2025-03-30' → 2025-03-29T15:00:00Z ~ 2025-03-30T15:00:00Z
    """
    KST = timezone(timedelta(hours=9))

    # 1️⃣ 입력 날짜 문자열을 datetime으로 (KST 기준)
    start_kst = datetime.strptime(kst_date_str, "%Y-%m-%d").replace(tzinfo=KST)
    end_kst = start_kst + timedelta(days=1)

    # 2️⃣ UTC로 변환
    start_utc = start_kst.astimezone(timezone.utc)
    end_utc = end_kst.astimezone(timezone.utc)

    return start_utc, end_utc

def get_data_by_date_and_category(kst_date_str, db_name, collection_name):
    """
    지정한 날짜부터 오늘까지의 데이터를 MongoDB에서 가져오고,
    카테고리별로 그룹화하여 반환합니다.

    Args:
        from_date_str (str): 시작 날짜 (예: '2023-10-01')
        db_name (str): MongoDB 데이터베이스 이름
        collection_name (str): 컬렉션 이름

    Returns:
        dict: {category_id: [video1, video2, ...], ...}
    """
    db = client[db_name]
    collection = db[collection_name]

    start_utc, end_utc = get_utc_range_from_kst_date(kst_date_str)

    print("쿼리 시작 시각 (UTC):", start_utc)
    print("쿼리 종료 시각 (UTC):", end_utc)

    query = {
        "timestamp": {
            "$gte": start_utc,
            "$lt": end_utc
        }
    }

    results = list(collection.find(query))
    print(f"📦 조회된 문서 수: {len(results)}")

    # 카테고리별로 그룹화
    grouped = defaultdict(list)
    for doc in results:
        cat_id = doc.get("metadata", {}).get("category_id")
        if cat_id:
            grouped[cat_id].append(doc)

    return dict(grouped)

def store_trending_videos_with_comments(db_name, collection_name):
    
    db = client[db_name]  # MongoDB 데이터베이스 이름
    collection = db[collection_name]  # MongoDB 컬렉션 이름
    
    for category_name, category_id in CATEGORIES.items():
        print(f"'{category_name}'동영상 가져오는 중...")

        # 1️⃣ 인기 동영상 가져오기
        videos = fetch_trending_videos(category_id, max_results=200)

        for video in videos:
            video_id = video["video_id"]

            # 2️⃣ 해당 동영상의 댓글 가져오기
            comments = fetch_video_comments(video_id, max_results=1000)
            cleaned_comments = [clean_text(comment, category_id) for comment in comments]
            
            document = {
                "timestamp": datetime.now(),  # 현재 시간 (UTC)
                "metadata": {
                    "category_id": category_id
                    },
                "video_id": video["video_id"],
                "title": video["title"],
                "description": video["description"],
                "tags": video["tags"],
                "duration": video["duration"],
                "view_count": video["view_count"],
                "like_count": video["like_count"],
                "comment_count": video["comment_count"],
                "published_at": video["published_at"],
                "subscriber_count": video["subscriber_count"],
                "comments": cleaned_comments  # 댓글 추가
            }
            collection.insert_one(document)
        
def store_combine_video_keyword_scores(data, db_name, collection_name):
    db = client[db_name]  # MongoDB 데이터베이스 이름
    collection = db[collection_name]  # MongoDB 컬렉션 이름
    
    for category, videos in data.items():
        for video in videos:
            combined_scores = {}
            # 빈도수 기반 score
            for keyword, score in video.get("freq_score", {}).items():
                combined_scores[keyword] = combined_scores.get(keyword, 0) + score
            # 텍스트랭크 기반 score
            for keyword, score in video.get("text_score", {}).items():
                combined_scores[keyword] = combined_scores.get(keyword, 0) + score
            # tf-idf+KRWordRank 기반 score
            for keyword, score in video.get("tf_kr_score", {}).items():
                combined_scores[keyword] = combined_scores.get(keyword, 0) + score
            
            # 내림차순 정렬하여 combined_score에 저장
            sorted_scores = dict(sorted(combined_scores.items(), key=lambda x: x[1], reverse=True))
            video["combined_score"] = sorted_scores
    
    # MongoDB 연결 설정
    # "video_keywords" 컬렉션이 없으면 생성
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
    collection = db[collection_name]
        
    # ✅ 데이터 저장
    documents = []
    for category, videos in data.items():
        for video in videos:
            doc = {
                "timestamp": video.get("timestamp"),
                "video_id": video.get("video_id"),
                "category": category,
                "title": video.get("title"),
                "view_count": video.get("view_count", 0),
                "like_count": video.get("like_count", 0),
                "comment_count": video.get("comment_count", 0),
                "published_at": video.get("published_at"),
                "subscriber_count": video.get("subscriber_count", 0),
                "combined_score": video.get("combined_score", {})
            }
            documents.append(doc)

    if documents:
        collection.insert_many(documents)
        print(f"store_combine_video_keyword_scores : 총 {len(documents)}개의 키워드 분석 결과를 저장했습니다.")
    else:
        print("store_combine_video_keyword_scores : 저장할 데이터가 없습니다.")