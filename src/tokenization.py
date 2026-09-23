"""Kiwi 형태소 분석기를 이용해 영상 텍스트를 키워드 후보로 바꾸는 모듈입니다.

전처리된 문장을 단순히 공백으로 나누면 조사·어미·일반 동사까지 모두 단어로
남습니다. 이 모듈은 Kiwi 한국어 형태소 분석 결과에서 분석 목적에 적합한
품사만 선택해 제목, 태그, 댓글을 서로 다른 입력 신호로 저장합니다.

입력:
    video - title, tags, comments 필드를 가진 영상 딕셔너리
    kiwi  - 학습 또는 설정이 끝난 Kiwi 형태소 분석기 객체

출력:
    원본 영상 정보에 아래 필드가 추가된 새 딕셔너리
    title_nouns   - 제목에서 추출한 고유명사·외국어 후보
    tag_nouns     - 중복을 제거한 태그 후보
    comment_nouns - 모든 댓글에서 추출한 후보

선택 기준:
    - 고유명사 NNP와 외국어 SL을 우선 사용합니다.
    - 길이가 2자 미만인 토큰과 불용어는 제외합니다.
    - 이후 keyword_scoring 모듈이 세 입력 필드에 서로 다른 가중치를 줍니다.
"""

from __future__ import annotations  # 최신 타입 표기법을 안전하게 사용합니다.

from collections.abc import Iterable, Sequence  # 반복 가능한 입력 타입을 표현합니다.
from typing import Any  # Kiwi 객체처럼 외부 라이브러리 객체를 유연하게 받습니다.

# 분석에 의미가 적은 공통 표현을 기본 불용어로 정의합니다.
DEFAULT_STOPWORDS = {"사랑해요", "안녕하세요", "사랑합니다", "한국"}
# 고유명사(NNP)와 외국어(SL)를 핵심 키워드 후보 품사로 사용합니다.
TARGET_POS = {"NNP", "SL"}


def extract_candidates(
    text: str,
    kiwi: Any,
    stopwords: Iterable[str] = DEFAULT_STOPWORDS,
    target_pos: set[str] = TARGET_POS,
) -> list[str]:
    """문장에서 길이 2 이상인 의미 있는 후보 키워드를 추출합니다."""
    # 전달받은 Kiwi 모델로 문장을 형태소 단위로 분석합니다.
    tokens = kiwi.tokenize(text)
    # 반복 탐색을 빠르게 하기 위해 불용어를 집합으로 변환합니다.
    blocked = set(stopwords)
    # 품사·길이·불용어 조건을 모두 통과한 토큰 표면형만 반환합니다.
    return [
        token.form
        for token in tokens
        if token.tag in target_pos and len(token.form) > 1 and token.form not in blocked
    ]


def tokenize_video(
    video: dict[str, Any],
    kiwi: Any,
    stopwords: Iterable[str] = DEFAULT_STOPWORDS,
) -> dict[str, Any]:
    """영상 1개의 제목·태그·댓글에서 분석용 토큰 필드를 만듭니다."""
    # 원본 입력을 바꾸지 않도록 얕은 복사본을 생성합니다.
    result = dict(video)
    # 댓글이 없을 때도 안전하게 빈 리스트를 사용합니다.
    comments: Sequence[str] = result.get("comments", [])
    # 제목에서 고유명사·외국어 중심의 후보 키워드를 추출합니다.
    result["title_nouns"] = extract_candidates(result.get("title", ""), kiwi, stopwords)
    # 태그는 공백을 제거하고 두 글자 이상인 값만 중복 없이 저장합니다.
    result["tag_nouns"] = sorted(
        {tag.strip() for tag in result.get("tags", []) if len(tag.strip()) > 1}
    )
    # 여러 댓글을 하나의 문서로 합친 뒤 같은 기준으로 후보를 추출합니다.
    result["comment_nouns"] = extract_candidates("\n".join(comments), kiwi, stopwords)
    # 후속 점수화 단계가 사용할 토큰이 추가된 영상 레코드를 반환합니다.
    return result
