import json
from collections import defaultdict

# 파일 경로
ranking_path = "data/final_keywords_ranking.json"
score_path = "data/0330_final_score.json"
output_path = "data/keywords_to_videos.json"

# 파일 로딩
with open(ranking_path, "r", encoding="utf-8") as f:
    keyword_ranking = json.load(f)

with open(score_path, "r", encoding="utf-8") as f:
    score_data = json.load(f)

# 결과 저장용 딕셔너리
categorized_keyword_videos = defaultdict(lambda: defaultdict(list))

# 점수 데이터 순회
for category, videos in score_data.items():
    for video in videos:
        video_id = video.get("video_id")
        combined_score = video.get("combined_score", {})
        
        # 해당 카테고리의 키워드 랭킹이 없으면 skip
        if category not in keyword_ranking:
            continue
        ranked_keywords = keyword_ranking[category]
        
        for keyword in combined_score:
            if keyword in ranked_keywords:
                if len(categorized_keyword_videos[category][keyword]) < 10:
                    categorized_keyword_videos[category][keyword].append(video_id)

# 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(categorized_keyword_videos, f, ensure_ascii=False, indent=4)

print(f"✅ 카테고리별 키워드 → 관련 영상 리스트가 '{output_path}'에 저장되었습니다.")
