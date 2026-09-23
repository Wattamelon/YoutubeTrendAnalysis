"""from datetime import datetime, timezone, timedelta
from ranking_core import run_ranking
import json
import sys
sys.stdout.reconfigure(encoding="utf-8")
end = datetime.now(timezone.utc)
start = end - timedelta(days=30)

# ✅ 결과 반환받기
result = run_ranking(start, end)

# ✅ JSON만 출력하기 (중간에 print 메시지 없어야 백엔드에서 파싱 가능)
print(json.dumps(result, ensure_ascii=False))
"""

from datetime import datetime, timedelta
from ranking_core import get_period_range, find_closest_date, run_ranking_by_category, compare_rankings_by_category
import json
import sys
# ✅ stdout을 UTF-8로 설정 (한글 깨짐 방지)
sys.stdout.reconfigure(encoding="utf-8")

# 이번 달 날짜 범위
start, end, _ = get_period_range("month")

# 이번 달 랭킹 계산
month_ranking = run_ranking_by_category(start, end)

# 저번 달에 가장 가까운 날짜 찾기
closest_date = find_closest_date(start, 30)
if closest_date:
    closest_start = datetime.combine(closest_date, datetime.min.time())
    closest_end = closest_start + timedelta(days=30)
    past_ranking = run_ranking_by_category(closest_start, closest_end)
else:
    past_ranking = {}

# 비교 결과 출력
comparison = compare_rankings_by_category(month_ranking, past_ranking)
print(json.dumps(comparison, ensure_ascii=False, indent=2))
