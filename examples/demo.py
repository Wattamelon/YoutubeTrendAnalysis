"""Small deterministic example of the curated ranking modules.

Run from the repository root:
    python examples/demo.py
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.keyword_scoring import frequency_scores
from src.ranking import aggregate_scores, compare_rankings
from src.related_keywords import related_keywords
from src.related_videos import select_related_videos


videos = [
    {
        "title_nouns": ["방탄소년단"],
        "tag_nouns": ["방탄소년단", "컴백"],
        "comment_nouns": ["방탄소년단", "컴백", "무대", "방탄소년단"],
    },
    {
        "title_nouns": ["컴백"],
        "tag_nouns": ["음악"],
        "comment_nouns": ["컴백", "무대", "음악"],
    },
]

for video in videos:
    video["combined_score"] = frequency_scores(video)

current = aggregate_scores(videos)
previous = [{"keyword": "컴백", "score": 20}, {"keyword": "방탄소년단", "score": 10}]

print("Current ranking:", current)
print("Ranking movement:", compare_rankings(current, previous))
print(
    "Related keywords:",
    related_keywords(
        "방탄소년단",
        [["방탄소년단", "컴백", "무대", "음악", "팬"], ["방탄소년단", "컴백", "무대", "음악", "팬"]],
        min_cooccurrence=2,
    ),
)

# 동일 영상의 여러 수집 기록 중 키워드 점수가 가장 높은 기록만 남기는 예시입니다.
print(
    "Related videos:",
    select_related_videos(
        "방탄소년단",
        [
            {"video_id": "a", "title": "컴백 무대", "combined_score": {"방탄소년단": 80}},
            {"video_id": "a", "title": "컴백 무대", "combined_score": {"방탄소년단": 100}},
            {"video_id": "b", "title": "인터뷰", "combined_score": {"방탄소년단": 70}},
        ],
    ),
)
