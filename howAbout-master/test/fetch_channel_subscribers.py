import json
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

# 파일 경로
input_path = "data/keywords_to_videos.json"
output_path = "data/channel_subscribers.json"

# 영상 ID → 채널 ID 및 구독자 수 캐시
video_to_channel_info = {}

# 영상 ID → 채널 ID
def get_channel_id(video_id):
    try:
        response = youtube.videos().list(part="snippet", id=video_id).execute()
        return response["items"][0]["snippet"]["channelId"]
    except Exception as e:
        print(f"❌ Error getting channel ID for video {video_id}: {e}")
        return None

# 채널 ID → 구독자 수
def get_subscriber_count(channel_id):
    try:
        response = youtube.channels().list(part="statistics", id=channel_id).execute()
        return int(response["items"][0]["statistics"]["subscriberCount"])
    except Exception as e:
        print(f"❌ Error fetching subscriber count for channel {channel_id}: {e}")
        return None

# 파일 읽기
with open(input_path, "r", encoding="utf-8") as f:
    keywords_data = json.load(f)

# 최종 결과 저장 구조
output_data = {}

for category, keyword_dict in keywords_data.items():
    output_data[category] = {}
    for keyword, video_ids in keyword_dict.items():
        print(f"🔍 [카테고리: {category}] 키워드 '{keyword}'에 대한 채널 구독자 수 조회 중...")
        output_data[category][keyword] = {}
        for video_id in video_ids:
            if video_id in video_to_channel_info:
                output_data[category][keyword][video_id] = video_to_channel_info[video_id]
                continue

            channel_id = get_channel_id(video_id)
            if not channel_id:
                continue

            subscriber_count = get_subscriber_count(channel_id)
            if subscriber_count is None:
                continue

            video_to_channel_info[video_id] = {
                "channel_id": channel_id,
                "subscriber_count": subscriber_count
            }

            output_data[category][keyword][video_id] = video_to_channel_info[video_id]
            time.sleep(0.3)  # 쿼터 절약

# 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f"\n✅ 최종 결과가 '{output_path}'에 저장되었습니다.")
