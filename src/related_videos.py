"""선택한 키워드의 점수가 높은 최근 관련 영상을 반환하는 모듈입니다.

이 모듈은 키워드 랭킹 화면에서 사용자가 특정 키워드를 클릭했을 때,
그 키워드가 실제로 어떤 영상에서 중요하게 나타났는지 보여주기 위한 기능입니다.

원본 서비스 흐름:
    MongoDB에서 최근 기간의 영상 조회
    → combined_score 안에 선택한 키워드가 있는 영상만 선택
    → 같은 video_id의 중복 수집 기록 제거
    → 선택한 키워드의 점수가 높은 순으로 Top N 반환

입력 데이터:
    각 영상은 video_id, title, timestamp, combined_score를 포함합니다.
    combined_score는 keyword_scoring 모듈이 만든 {키워드: 점수} 사전입니다.

핵심 기준:
    이 모듈은 의미론적 임베딩 유사도로 영상을 추천하지 않습니다.
    선택한 키워드가 제목·태그·댓글 분석에서 높은 combined_score를 받은
    영상을 '관련 영상'으로 정의합니다.

데이터 수집이 반복되면 같은 영상이 여러 날짜에 저장될 수 있습니다.
따라서 video_id 기준으로 중복을 제거하고, 가장 높은 키워드 점수만 유지합니다.
"""

from __future__ import annotations  # 최신 타입 표기법을 안전하게 사용합니다.

from collections.abc import Iterable, Mapping  # 입력 영상 목록과 점수 사전 타입을 표현합니다.
from datetime import datetime, timedelta, timezone  # 최근 기간 계산과 MongoDB 시간 조건에 사용합니다.
from typing import Any  # JSON 형태의 유연한 영상 레코드 타입에 사용합니다.


def build_recent_related_video_query(
    keyword: str,
    days: int = 30,
    now: datetime | None = None,
) -> dict[str, Any]:
    """MongoDB에서 최근 관련 영상을 조회할 조건을 생성합니다."""
    # 테스트나 배치 실행에서 기준 시각을 고정할 수 있도록 now를 선택적으로 받습니다.
    now = now or datetime.now(timezone.utc)
    # 최근 days일의 시작 시각을 계산합니다.
    since = now - timedelta(days=days)
    # combined_score 안에 키워드 필드가 존재하는 최근 영상만 찾는 MongoDB 조건입니다.
    return {
        f"combined_score.{keyword}": {"$exists": True},
        "timestamp": {"$gte": since},
    }


def select_related_videos(
    keyword: str,
    documents: Iterable[Mapping[str, Any]],
    top_n: int = 5,
) -> list[dict[str, Any]]:
    """조회된 영상에서 키워드 점수가 높은 중복 없는 Top N을 반환합니다."""
    # video_id별로 현재까지 가장 좋은 기록을 보관합니다.
    best_by_video: dict[str, dict[str, Any]] = {}

    # MongoDB에서 조회했거나 테스트에서 전달한 영상 레코드를 하나씩 확인합니다.
    for document in documents:
        # 선택한 키워드가 없는 영상은 관련 영상 후보가 아니므로 건너뜁니다.
        scores = document.get("combined_score", {})
        if keyword not in scores:
            continue

        # video_id가 없으면 같은 영상인지 판별할 수 없어 안전하게 제외합니다.
        video_id = document.get("video_id")
        if not video_id:
            continue

        # 선택한 키워드의 영상별 combined_score를 숫자로 변환합니다.
        score = float(scores[keyword])
        # 현재 영상에서 UI에 필요한 필드만 새 레코드로 만듭니다.
        candidate = {
            "video_id": video_id,
            "title": document.get("title", ""),
            "score": score,
            "timestamp": document.get("timestamp"),
        }

        # 처음 본 영상이거나, 이전 기록보다 키워드 점수가 높을 때만 교체합니다.
        if video_id not in best_by_video or score > best_by_video[video_id]["score"]:
            best_by_video[video_id] = candidate

    # 서로 다른 영상만 남긴 뒤 키워드 점수가 높은 순으로 정렬합니다.
    ordered = sorted(best_by_video.values(), key=lambda video: -float(video["score"]))
    # 화면에 표시할 상위 top_n개 영상만 반환합니다.
    return ordered[:top_n]
