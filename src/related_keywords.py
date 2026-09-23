"""댓글 N-gram 동시 출현과 PMI로 연관 키워드를 계산하는 모듈입니다.

키워드 랭킹은 어떤 주제가 뜨는지 보여 주지만, 사용자는 그 주제와 함께
어떤 인물·사건·콘텐츠가 언급되는지도 알고 싶습니다. 이 모듈은 대상 키워드와
같은 댓글 문맥에 함께 나타나는 단어를 찾아 연관 키워드로 제시합니다.

입력:
    target       - 연관어를 찾을 기준 키워드
    video_tokens - 영상별 댓글 토큰 열의 반복 가능한 목록

출력:
    keyword와 score를 가진 연관 키워드 목록. 점수가 높은 순으로 반환합니다.

계산 방식:
    1. 각 영상의 댓글 토큰에서 길이 n의 연속 N-gram을 생성합니다.
    2. 대상 키워드가 포함된 N-gram 안의 다른 단어를 연관 후보로 모읍니다.
    3. 한 영상에서 여러 번 언급되어도 영상 단위로 한 번만 세어 반복 댓글
       또는 스팸의 영향을 줄입니다.
    4. PMI로 실제 동시 출현이 독립적으로 기대되는 수준보다 강한지 계산합니다.
    5. PMI에 동시 출현 영상 수를 곱해 강도와 빈도를 함께 반영합니다.

PMI만 사용하면 드물게 한 번 함께 등장한 단어가 과대평가될 수 있으므로,
min_cooccurrence로 최소 동시 출현 횟수를 지정합니다.
"""

from __future__ import annotations  # 최신 타입 표기법을 안전하게 사용합니다.

from collections import Counter  # 영상 단위 출현·동시 출현 횟수를 셉니다.
from collections.abc import Iterable, Sequence  # 토큰 문서 입력 타입을 표현합니다.
from math import log  # PMI 계산의 로그 함수에 사용합니다.


def _ngrams(tokens: Sequence[str], size: int) -> Iterable[tuple[str, ...]]:
    """토큰 열에서 지정한 길이의 연속 N-gram을 하나씩 생성합니다."""
    # 만들 수 있는 마지막 시작 위치까지 반복합니다.
    for index in range(len(tokens) - size + 1):
        # 현재 위치부터 size개 토큰을 잘라 튜플로 반환합니다.
        yield tuple(tokens[index : index + size])


def related_keywords(
    target: str,
    video_tokens: Iterable[Sequence[str]],
    ngram_size: int = 5,
    min_cooccurrence: int = 2,
    top_n: int = 20,
) -> list[dict[str, float | str]]:
    """대상 키워드와 강하게 함께 등장한 키워드를 PMI × 빈도로 정렬합니다."""
    # 반복 가능한 입력을 한 번만 순회해도 되도록 리스트로 고정합니다.
    documents = list(video_tokens)
    # 확률 계산의 분모가 되는 전체 영상 수를 구합니다.
    total_videos = len(documents)
    # 입력 영상이 없으면 계산할 수 없으므로 빈 결과를 반환합니다.
    if not total_videos:
        return []

    # 각 단어가 등장한 영상 수를 저장합니다.
    term_frequency: Counter[str] = Counter()
    # 대상 키워드와 같은 N-gram에 등장한 영상 수를 저장합니다.
    cooccurrence: Counter[str] = Counter()
    # 대상 키워드가 등장한 영상 수를 저장합니다.
    target_videos = 0

    # 영상 하나당 토큰 열 하나를 순회합니다.
    for tokens in documents:
        # 같은 영상에서 여러 번 등장해도 영상 단위로 한 번만 세기 위한 집합입니다.
        seen_terms, related_terms = set(), set()
        # 이 영상에서 대상 키워드를 포함한 N-gram이 있었는지 기록합니다.
        contains_target = False
        # 모든 연속 N-gram을 만들며 동시 출현을 확인합니다.
        for gram in _ngrams(tokens, ngram_size):
            # 현재 N-gram의 모든 단어를 이 영상의 등장 단어로 추가합니다.
            seen_terms.update(gram)
            # 대상 키워드가 N-gram 안에 있으면 연관 후보를 모읍니다.
            if target in gram:
                contains_target = True
                related_terms.update(term for term in gram if term != target)
        # 대상 키워드를 제외한 단어의 영상 단위 출현 수를 증가시킵니다.
        term_frequency.update(seen_terms - {target})
        # 대상 키워드가 있었을 때만 대상 영상 수와 동시 출현 수를 증가시킵니다.
        if contains_target:
            target_videos += 1
            cooccurrence.update(related_terms)

    # 대상 키워드가 어떤 영상에도 없으면 연관 키워드가 없습니다.
    if not target_videos:
        return []

    # 대상 키워드가 등장한 영상 비율을 계산합니다.
    target_probability = target_videos / total_videos
    # PMI와 빈도를 결합한 결과를 저장할 리스트입니다.
    ranked = []
    # 대상 키워드와 함께 등장한 모든 후보 단어를 순회합니다.
    for term, count in cooccurrence.items():
        # 최소 동시 출현 횟수보다 적으면 우연한 연관일 수 있어 제외합니다.
        if count < min_cooccurrence:
            continue
        # 후보 단어가 등장한 영상 비율을 계산합니다.
        term_probability = term_frequency[term] / total_videos
        # 대상·후보가 함께 등장한 영상 비율을 계산합니다.
        joint_probability = count / total_videos
        # PMI는 실제 동시 출현이 독립적 기대값보다 강한지를 측정합니다.
        pmi = log((joint_probability / (target_probability * term_probability)) + 1e-12)
        # PMI에 동시 출현 횟수를 곱해 강도와 빈도를 함께 반영합니다.
        ranked.append({"keyword": term, "score": round(pmi * count, 5)})

    # 점수가 높은 순으로 정렬하고, 동점이면 키워드 이름 순으로 안정적으로 정렬합니다.
    return sorted(
        ranked, key=lambda row: (-float(row["score"]), str(row["keyword"]))
    )[:top_n]
