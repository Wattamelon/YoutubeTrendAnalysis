""" 
안녕 지훈아
이제부터 내 똥코드 설명을 시작할게.

이 코드는 트렌드 스코어를 만드는 코드야. 
영상별로 추출된 combined socre에 정규화된 조회수랑 좋아요수를 곱해서 (조회수, 좋아요수에 가중치를 부여해서)
trend_score.json을 추출하게 했어.
근데 , 우리는 이 트렌드 스코어를 사용해서 날짜별로 트렌드 변동 추이를 보여줘야 하니까 날짜_trend.json 으로 생성되게 했어.

"""
import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os
from datetime import datetime

# 오늘 날짜 가져오기
today_str = datetime.now().strftime("%m%d")  

# 파일 경로
video_path = f"/Users/melon/third_pre/youtube/last/data/{today_str}_final_score.json"
keyword_path = f"/Users/melon/third_pre/youtube/last/data/{today_str}_category_keywords.json"

# 파일 로딩
with open(video_path, "r", encoding="utf-8") as f:
    video_data = json.load(f)

with open(keyword_path, "r", encoding="utf-8") as f:
    category_keywords = json.load(f)

# 1. view_count, like_count 정규화
all_videos = []
for category, videos in video_data.items():
    for video in videos:
        video_id = video.get("video_id")
        view_count = video.get("view_count", 0)
        like_count = video.get("like_count", 0)
        combined_score = video.get("combined_score", {})
        all_videos.append({
            "video_id": video_id,
            "category": category,
            "view_count": view_count,
            "like_count": like_count,
            "combined_score": combined_score
        })

df_videos = pd.DataFrame(all_videos)

# 정규화 (view_count, like_count)
scaler = MinMaxScaler()
df_videos[["view_norm", "like_norm"]] = scaler.fit_transform(df_videos[["view_count", "like_count"]])

# 2-3. 키워드별 점수 계산
keyword_scores = {}

for _, row in df_videos.iterrows():
    combined_score = row["combined_score"]
    view_norm = row["view_norm"]
    like_norm = row["like_norm"]
    
    for keyword, score in combined_score.items():
        weight = (view_norm + like_norm) * score
        if keyword not in keyword_scores:
            keyword_scores[keyword] = 0
        keyword_scores[keyword] += weight

# 4. 카테고리 랭킹 기반 가중치 반영
# 랭킹: 상위 1위 = 100점, 2위 = 99점 ... 100위 = 1점
for category, keywords in category_keywords.items():
    for rank, keyword in enumerate(keywords):
        if keyword in keyword_scores:
            keyword_scores[keyword] += (100 - rank)

# 결과를 DataFrame으로 정리
df_keyword_scores = pd.DataFrame(keyword_scores.items(), columns=["keyword", "score"])
df_keyword_scores = df_keyword_scores.sort_values(by="score", ascending=False)

# trend.json 파일로 저장
# 저장 경로 설정
output_path = f"/Users/melon/third_pre/youtube/last/data/{today_str}_trend.json"
df_keyword_scores.to_json(output_path, orient="records", force_ascii=False, indent=4)

