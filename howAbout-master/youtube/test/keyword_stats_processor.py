""" 
keyword_stats_summary.json 불러와서
preference (선호도) , engagement (참여도) 계산하는 코드야.
키워드별로 
선호도 = 좋아요수 / 조회수
참여도 = 댓글수 / 조회수
로 했어.

정규화된 선호도랑 참여도도 추출하긴 했는데 , 사용은 안하고 있어.

결과는 keyword_stats_summary.json으로 저장 
"""

import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 파일 로딩
with open("keyword_stats_summary.json", "r", encoding="utf-8") as f:
    keyword_stats = json.load(f)

# 카테고리별 키워드 데이터 정리
records = []
for category, keywords in keyword_stats.items():
    for keyword, stats in keywords.items():
        record = {
            "category": category,
            "keyword": keyword,
            "view_count": stats["view_count"],
            "like_count": stats["like_count"],
            "comment_count": stats["comment_count"],
        }
        # 선호도, 참여도 계산
        record["preference"] = stats["like_count"] / stats["view_count"] if stats["view_count"] > 0 else 0
        record["engagement"] = stats["comment_count"] / stats["view_count"] if stats["view_count"] > 0 else 0
        records.append(record)

df = pd.DataFrame(records)

# 선호도와 참여도 정규화
scaler = MinMaxScaler()
df[["normalized_preference", "normalized_engagement"]] = scaler.fit_transform(df[["preference", "engagement"]])

# JSON으로 저장할 구조로 변환
output = {}
for _, row in df.iterrows():
    cat = row["category"]
    if cat not in output:
        output[cat] = {}
    output[cat][row["keyword"]] = {
        "view_count": int(row["view_count"]),
        "like_count": int(row["like_count"]),
        "comment_count": int(row["comment_count"]),
        "preference": round(row["preference"], 5),
        "engagement": round(row["engagement"], 5),
        "normalized_preference": round(row["normalized_preference"], 5),
        "normalized_engagement": round(row["normalized_engagement"], 5),
    }

# 저장
output_path = "keyword_stats_with_scores.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

output_path
