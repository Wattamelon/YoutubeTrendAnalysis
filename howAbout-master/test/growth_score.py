import json

# 파일 경로
video_data_path = "data/0330_raw_video_data.json"
subscriber_data_path = "data/channel_subscribers.json"
output_path = "data/keyword_growth_score.json"

# 파일 로드
with open(video_data_path, "r", encoding="utf-8") as f:
    video_data = json.load(f)

with open(subscriber_data_path, "r", encoding="utf-8") as f:
    channel_subscribers = json.load(f)

# video_id -> view_count 매핑
video_views = {}
for category, videos in video_data.items():
    for video in videos:
        vid = video.get("video_id")
        view_count = video.get("view_count", 0)
        if vid:
            video_views[vid] = view_count

# 키워드 성장 가능성 계산
keyword_growth_scores = {}

for category, keyword_map in channel_subscribers.items():
    keyword_growth_scores[category] = {}
    for keyword, video_info in keyword_map.items():
        print(f"📊 계산 중: [{category}] 카테고리 - 키워드 '{keyword}'")

        weighted_total = 0
        total_subscribers = 0

        for vid, info in video_info.items():
            view_count = video_views.get(vid, 0)
            subs = info.get("subscriber_count", 0)

            if subs > 0:
                efficiency = view_count / subs
                weighted_total += efficiency * subs
                total_subscribers += subs

        if total_subscribers > 0:
            growth_score = weighted_total / total_subscribers
            keyword_growth_scores[category][keyword] = growth_score

# 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(keyword_growth_scores, f, ensure_ascii=False, indent=4)

print(f"\n✅ 성장 가능성 분석 결과가 '{output_path}'에 저장되었습니다.")
