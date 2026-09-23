""" 
이거 실행하면 trend_timeseries.csv 가 생성돼.
시계열 데이터로 앞으로의 키워드 트랜드의 변화를 예측하기 위해 날짜_trend.json 을 모두 불러와서 csv 파일로 저장해.
그게 끝이야 여긴.
"""

import os
import json
import pandas as pd

# trend 파일들이 들어있는 디렉토리
trend_folder = "./data"

# 날짜별 trend 데이터 읽기
trend_data_by_date = {}

for filename in os.listdir(trend_folder):
    if filename.endswith("_trend.json"):
        date_key = filename.replace("_trend.json", "")  # e.g., "0326"
        file_path = os.path.join(trend_folder, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for entry in data:
            keyword = entry["keyword"]
            score = entry["score"]
            if keyword not in trend_data_by_date:
                trend_data_by_date[keyword] = {}
            trend_data_by_date[keyword][date_key] = score

# DataFrame 생성 (keyword 기준으로 index, 날짜 기준으로 column)
df_trend = pd.DataFrame.from_dict(trend_data_by_date, orient="index")
df_trend = df_trend.sort_index(axis=1)  # 날짜순 정렬

# 결과 확인용 CSV 저장
df_trend.to_csv("./data/trend_timeseries.csv", encoding="utf-8-sig")

print("✅ 키워드별 시계열 데이터 생성 완료!")
