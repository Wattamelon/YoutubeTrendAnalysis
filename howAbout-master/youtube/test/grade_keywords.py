""" 
마지막으로 모든 키워드의 선호도랑 참여도를 확인해서
키워드별의 선호도랑 참여도를 A~B 까지 등급을 매겼어. 상위 25%는 A , 25 ~50 은 B 이런식으로

"""

import json
import numpy as np

# 파일 로드
with open("keyword_stats_with_scores.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 등급 구간 분할 함수
def assign_grade(value, quartiles):
    if value <= quartiles[0]:
        return "D"
    elif value <= quartiles[1]:
        return "C"
    elif value <= quartiles[2]:
        return "B"
    else:
        return "A"

# 카테고리별 등급 매기기
for category, keywords in data.items():
    preferences = []
    engagements = []

    for info in keywords.values():
        if "preference" in info and "engagement" in info:
            preferences.append(info["preference"])
            engagements.append(info["engagement"])

    if not preferences or not engagements:
        continue

    # 사분위수 계산
    pref_quartiles = np.percentile(preferences, [25, 50, 75])
    eng_quartiles = np.percentile(engagements, [25, 50, 75])

    for keyword, info in keywords.items():
        pref_val = info.get("preference")
        eng_val = info.get("engagement")

        if pref_val is not None:
            info["preference_grade"] = assign_grade(pref_val, pref_quartiles)
        if eng_val is not None:
            info["engagement_grade"] = assign_grade(eng_val, eng_quartiles)

# 저장
output_path = "graded_keywords.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"✅ 등급이 '{output_path}'에 저장되었습니다.")
