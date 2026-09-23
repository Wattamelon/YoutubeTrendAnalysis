"""from datetime import datetime, timezone, timedelta
from ranking_core import run_ranking
import json
import sys
# 📅 지난 7일간
sys.stdout.reconfigure(encoding="utf-8")
end = datetime.now(timezone.utc)
start = end - timedelta(days=7)

# 🟢 결과 반환
result = run_ranking(start, end)

# ✅ JSON만 출력
print(json.dumps(result, ensure_ascii=False))
"""


from datetime import datetime, timedelta
from ranking_core import get_period_range, find_closest_date, run_ranking_by_category, compare_rankings_by_category
import json
import sys
# ✅ stdout을 UTF-8로 설정 (한글 깨짐 방지)
sys.stdout.reconfigure(encoding="utf-8")

# 이번 주 날짜 범위
start, end, _ = get_period_range("week")

# 이번 주 랭킹 계산
week_ranking = run_ranking_by_category(start, end)

# 저번 주에 가장 가까운 날짜 찾기
closest_date = find_closest_date(start, 7)
if closest_date:
    closest_start = datetime.combine(closest_date, datetime.min.time())
    closest_end = closest_start + timedelta(days=7)
    past_ranking = run_ranking_by_category(closest_start, closest_end)
else:
    past_ranking = {}

# 비교 결과 출력
comparison = compare_rankings_by_category(week_ranking, past_ranking)
print(json.dumps(comparison, ensure_ascii=False, indent=2))

