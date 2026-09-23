from init import *
from kiwi import make_kiwi
from datetime import datetime, timedelta, timezone
from mongo_connect import *
from tokenize_video import tokenize_video
from analyze import *
CATEGORIES = {
    "News & Politics": "25",
    'Music' : "10",
    'Sports' : "17",
    'Gaming' : "20",
    'Science & Technology': "28"
}

def main():
    
    # 1. 동영상 데이터 가져오고 저장하기기
    #store_trending_videos_with_comments(db_name="raw_video_data", collection_name="raw_video_data")
    # 2. 데이터 가져오기
    data = get_data_by_date_and_category(kst_date_str= "2025-06-23", db_name= "raw_video_data",collection_name="raw_video_data")
    # 3. kiwi 학습하기
    kiwi_objects = make_kiwi(data)
    # 4.tokenize하기
    proceesd_data = tokenize_video(data, kiwi_objects)
    # 5. 키워드 점수 매기기
    scored_data = score_video_keywords(proceesd_data)
    # 6. 키워드 점수 합치기, 저장
    store_combine_video_keyword_scores(db_name= "keyword", collection_name= "keyword", data = scored_data)

    
if __name__ == "__main__":
    main()