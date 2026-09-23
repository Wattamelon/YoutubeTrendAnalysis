""" 
최종 키워드 랭킹 (final_keywords_ranking.json) 의 키워드들별로
그 키워드가 combined_score에 들어있는 영상들의
총 조회수 , 총 좋아요 수 , 총 댓글수를 계산했어.
예를들어 a영상의 combined_score에 이재명 키워드가 있으면 
이재명 키워드의 조회수에 그 영상의 조회수가 추가되는 식으로 ㅇㅇ 
그래서 keyword_stats_summary.json 생성되게 했어.
여긴 그게 끝
0330_raw_video_data.json은 왜 넣었냐면 , 내 0330_final_score.json에는 영상 조회수 좋아요 댓글수가 다 null로 나와서 그냥 raw 데이터에서 조회수 좋아요 댓글수 가져왔어.
이건 너꺼에서 수정해서 final_score.json에서 조회수 좋아요 댓글수 가져오게 하면 될거같아.
"""

import json
from collections import defaultdict
import pandas as pd

# 파일 경로
score_path = "data/0330_final_score.json"
ranking_path = "data/final_keywords_ranking.json"
raw_path = "data/0330_raw_video_data.json"
output_path = "keyword_stats_summary.json"

# 파일 로딩
with open(score_path, "r", encoding="utf-8") as f:
    video_data = json.load(f)

with open(ranking_path, "r", encoding="utf-8") as f:
    keyword_ranking = json.load(f)

with open(raw_path, "r", encoding="utf-8") as f:
    raw_video_data = json.load(f)

# 1. 카테고리별 키워드 리스트 추출
category_keywords = {
    category: set(keywords)
    for category, keywords in keyword_ranking.items()
}

# 2. video_id → raw 정보 맵핑
video_id_to_info = {}
for category, videos in raw_video_data.items():
    for video in videos:
        video_id = video.get("video_id")
        if video_id:
            video_id_to_info[video_id] = {
                "view_count": video.get("view_count", 0) or 0,
                "like_count": video.get("like_count", 0) or 0,
                "comment_count": video.get("comment_count", 0) or 0,
            }

# 3. 결과 저장용 딕셔너리 (카테고리별로)
category_stats = {
    category: defaultdict(lambda: {"view_count": 0, "like_count": 0, "comment_count": 0})
    for category in category_keywords
}

# 4. 영상 데이터 순회하며 키워드 매칭 및 통계 집계
for category, videos in video_data.items():
    for video in videos:
        video_id = video.get("video_id")
        combined_score = video.get("combined_score", {})
        counts = video_id_to_info.get(video_id, {"view_count": 0, "like_count": 0, "comment_count": 0})

        # 각 카테고리별 키워드에 대해 확인
        for target_category, keywords in category_keywords.items():
            for keyword in combined_score:
                if keyword in keywords:
                    category_stats[target_category][keyword]["view_count"] += counts["view_count"]
                    category_stats[target_category][keyword]["like_count"] += counts["like_count"]
                    category_stats[target_category][keyword]["comment_count"] += counts["comment_count"]

# 5. defaultdict → 일반 dict로 변환
final_result = {
    category: dict(stats)
    for category, stats in category_stats.items()
}

# 6. JSON 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_result, f, ensure_ascii=False, indent=4)

print(f"✅ 카테고리별 키워드 통계가 '{output_path}'로 저장되었습니다.")
