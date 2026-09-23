""" 
아까만든 csv 파일에 있는 키워드별 트렌드 점수 변동 추이를 이용해서
prophet이라는 시계열 기법을 이용해서 앞으로의 트렌드 점수를 예측해서 결과를 predicted_trend.json으로 생성해줘.
솔직히 Prophet이 정확히 뭔지는 모르겠는데 , 결과는 선형적이야. 
"""

import pandas as pd
from prophet import Prophet
import json

# 1. 데이터 로딩 및 전처리
df = pd.read_csv("/Users/melon/third_pre/youtube/last/data/trend_timeseries.csv", index_col=0)
df = df.T.reset_index().rename(columns={"index": "ds"})
df["ds"] = pd.to_datetime("25" + df["ds"], format="%y%m%d")

# 2. 최신 날짜 기준 상위 3개 키워드 추출
latest_date = df["ds"].max()
top_keywords = df[df["ds"] == latest_date].drop(columns=["ds"]).T.squeeze().sort_values(ascending=False).head(20).index.tolist()

# 3. 예측 수행 및 결과 저장
result = {}

for keyword in top_keywords:
    df_keyword = df[["ds", keyword]].rename(columns={keyword: "y"})
    
    model = Prophet()
    model.fit(df_keyword)

    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)

    # 날짜 형식을 MMDD로 다시 변환
    forecast["ds_str"] = forecast["ds"].dt.strftime("%m%d")
    predicted_scores = dict(zip(forecast["ds_str"], forecast["yhat"].round(2)))

    result[keyword] = predicted_scores

# 4. JSON 저장
with open("predicted_trend.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("✅ 예측 결과 저장 완료: predicted_trend.json")
