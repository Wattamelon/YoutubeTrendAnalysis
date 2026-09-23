"""from datetime import datetime, timezone, timedelta
from ranking_core import run_ranking
import sys
# 현재 시간 (UTC 기준)
sys.stdout.reconfigure(encoding="utf-8")
now = datetime.now(timezone.utc)
start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc) - timedelta(days=1)
end = start + timedelta(days=2)

# 결과값 받아오기
result = run_ranking(start, end)

# ✅ 딱 JSON만 출력
import json
print(json.dumps(result, ensure_ascii=False))
"""

from datetime import datetime , timedelta
from ranking_core import get_period_range, find_closest_date, run_ranking_by_category, compare_rankings_by_category
import json
import sys
# ✅ stdout을 UTF-8로 설정 (한글 깨짐 방지)
sys.stdout.reconfigure(encoding="utf-8")

# 오늘 날짜 범위
start, end, _ = get_period_range("today")

# 오늘 랭킹 계산
today_ranking = run_ranking_by_category(start, end)

# 어제에 가장 가까운 날짜 찾기
closest_date = find_closest_date(start, 1)
if closest_date:
    closest_start = datetime.combine(closest_date, datetime.min.time())
    closest_end = closest_start + timedelta(days=1)
    past_ranking = run_ranking_by_category(closest_start, closest_end)
else:
    past_ranking = {}

# 비교 결과 출력
comparison = compare_rankings_by_category(today_ranking, past_ranking)
print(json.dumps(comparison, ensure_ascii=False, indent=2))
