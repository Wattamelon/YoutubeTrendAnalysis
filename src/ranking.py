"""영상별 키워드 점수를 기간 단위 랭킹으로 바꾸고 순위 변동을 계산하는 모듈입니다.

keyword_scoring 모듈은 영상 한 편 안에서 각 키워드가 얼마나 중요한지
combined_score로 계산합니다. 이 모듈은 같은 날짜·주·월과 같은 카테고리에
속한 여러 영상의 combined_score를 합산해 최종 키워드 순위를 만듭니다.

입력:
    aggregate_scores
        - 선택한 기간과 카테고리에 속한 영상 목록
        - 각 영상은 combined_score 사전을 포함해야 함
    compare_rankings
        - 현재 기간 랭킹과 이전 비교 기간 랭킹

출력:
    - keyword와 누적 score를 가진 내림차순 랭킹 목록
    - current_rank, previous_rank, rank_change, movement를 포함한 비교 목록

movement 값의 의미:
    rising      - 이전보다 순위가 상승
    falling     - 이전보다 순위가 하락
    unchanged   - 순위가 동일
    new         - 이전 Top K에는 없고 현재 Top K에 새로 진입
    ranked_out  - 이전 Top K에는 있었지만 현재 Top K에서 이탈

view_velocity_score는 초기 실험에서 사용한 시간당 조회수 보정 함수입니다.
현재 기본 랭킹은 combined_score 합산을 사용하며, 이 함수는 인기 반응 속도를
별도 신호로 결합할 수 있는 실험적 확장 지점으로 남겨두었습니다.
"""

from __future__ import annotations  # 최신 타입 표기법을 안전하게 사용합니다.

from collections import defaultdict  # 키워드별 합산 점수의 기본값을 0으로 처리합니다.
from collections.abc import Iterable  # 반복 가능한 영상 입력을 표현합니다.
from typing import Any  # JSON 형태의 유연한 레코드 타입에 사용합니다.


def aggregate_scores(videos: Iterable[dict[str, Any]]) -> list[dict[str, float | str]]:
    """여러 영상의 combined_score를 더해 내림차순 키워드 랭킹을 만듭니다."""
    # 키워드별 기간 누적 점수를 저장합니다.
    totals: defaultdict[str, float] = defaultdict(float)
    # 선택한 기간·카테고리에 포함된 모든 영상을 순회합니다.
    for video in videos:
        # 각 영상에 이미 계산된 combined_score를 꺼냅니다.
        for keyword, score in video.get("combined_score", {}).items():
            # 동일 키워드가 여러 영상에 등장하면 점수를 합산합니다.
            totals[keyword] += float(score)
    # 누적 점수를 큰 순서로 정렬하고 API/UI가 쓰기 쉬운 레코드로 변환합니다.
    return [
        {"keyword": keyword, "score": round(score, 3)}
        for keyword, score in sorted(totals.items(), key=lambda item: item[1], reverse=True)
    ]


def compare_rankings(
    current: list[dict[str, Any]],
    previous: list[dict[str, Any]],
    top_k: int = 30,
) -> list[dict[str, Any]]:
    """현재·이전 Top K를 비교해 상승, 하락, 신규, 랭크 아웃을 판별합니다."""
    # 현재 랭킹을 키워드에서 1부터 시작하는 순위로 변환합니다.
    current_rank = {row["keyword"]: index for index, row in enumerate(current[:top_k], 1)}
    # 이전 랭킹도 같은 형태로 변환합니다.
    previous_rank = {row["keyword"]: index for index, row in enumerate(previous[:top_k], 1)}

    # 비교 결과 레코드를 저장할 리스트입니다.
    comparison = []
    # 두 기간 중 한 번이라도 등장한 모든 키워드를 비교합니다.
    for keyword in current_rank.keys() | previous_rank.keys():
        # 현재·이전 순위를 각각 가져오며, 없으면 None을 사용합니다.
        now, before = current_rank.get(keyword), previous_rank.get(keyword)
        # 두 기간에 모두 있으면 이전 순위에서 현재 순위를 빼 등락을 계산합니다.
        change = before - now if now and before else None
        # 등장 여부와 등락 값으로 상태 라벨을 정합니다.
        movement = (
            "new" if now and not before else
            "ranked_out" if before and not now else
            "rising" if change and change > 0 else
            "falling" if change and change < 0 else
            "unchanged"
        )
        # 화면·API에서 바로 쓸 수 있는 비교 레코드를 추가합니다.
        comparison.append(
            {"keyword": keyword, "current_rank": now, "previous_rank": before,
             "rank_change": change, "movement": movement}
        )
    # 현재 순위가 있는 키워드를 먼저 보여 주고, 랭크 아웃은 뒤로 보냅니다.
    return sorted(comparison, key=lambda row: row["current_rank"] or float("inf"))


def view_velocity_score(video: dict[str, Any], elapsed_hours: float) -> float:
    """초기 실험에서 사용한 시간당 조회수 기반 인기 보정값을 계산합니다."""
    # 게시 이후 시간이 0 이하라면 0으로 나누지 않도록 0을 반환합니다.
    if elapsed_hours <= 0:
        return 0.0
    # 조회수를 게시 후 경과 시간으로 나눠 조회 속도를 반환합니다.
    return float(video.get("view_count", 0)) / elapsed_hours
