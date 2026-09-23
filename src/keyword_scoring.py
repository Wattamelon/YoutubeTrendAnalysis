"""빈도·문맥·코퍼스 중요도를 결합해 영상별 키워드 점수를 만드는 모듈입니다.

이 프로젝트의 핵심 모듈입니다. 키워드가 댓글에 많이 등장했다는 사실만으로
트렌드라고 판단하지 않습니다. 영상이 직접 다루는 주제인지, 댓글 문맥에서
중심적인지, 같은 카테고리의 다른 영상과 비교해 특징적인지를 함께 반영합니다.

입력:
    tokenization 모듈이 만든 title_nouns, tag_nouns, comment_nouns 필드를
    포함한 같은 카테고리의 영상 목록

출력:
    각 영상에 다음 점수 사전을 추가한 새 영상 목록
    frequency_score        - 제목·태그·댓글 출처별 빈도 점수
    textrank_score          - 댓글 동시 출현 그래프의 문맥 중심성 점수
    tfidf_krwordrank_score  - 카테고리 코퍼스 내 상대적 중요도 점수
    combined_score          - 세 점수를 동일 가중치로 합친 최종 점수

점수 설계:
    1. 제목은 직접적인 주제 신호이므로 30점, 태그는 10점을 부여합니다.
    2. 댓글은 등장할 때마다 0.1점씩 더해 반복 언급을 반영합니다.
    3. TextRank는 댓글 안에서 다른 중요한 단어와 많이 연결된 키워드를 찾습니다.
    4. TF-IDF와 KRWordRank의 곱은 흔한 단어를 낮추고 카테고리 내 특징적인
       키워드를 높입니다.
    5. TextRank와 TF-IDF/KRWordRank는 상위 50개의 순위를 50점부터 1점으로
       바꿔 서로 비교 가능한 스케일로 맞춥니다.

이 모듈의 combined_score는 ranking 모듈이 여러 영상을 집계할 때 사용하는
기본 단위입니다.
"""

from __future__ import annotations  # 최신 타입 표기법을 안전하게 사용합니다.

from collections import defaultdict  # 키워드별 누적 점수의 기본값을 0으로 처리합니다.
from collections.abc import Sequence  # 영상 목록과 토큰 목록의 타입을 표현합니다.
from typing import Any  # JSON 형태의 유연한 영상 레코드 타입에 사용합니다.

# 제목은 영상의 직접적인 주제라는 가정으로 가장 높은 가중치를 사용합니다.
TITLE_WEIGHT = 30.0
# 태그는 제목을 보조하는 구조화 메타데이터이므로 중간 가중치를 사용합니다.
TAG_WEIGHT = 10.0
# 댓글은 반복 언급을 반영하되 대량 댓글이 제목 신호를 압도하지 않게 낮게 설정합니다.
COMMENT_WEIGHT = 0.1
# TextRank와 TF-IDF/KRWordRank에서 보관할 최대 키워드 수입니다.
TOP_N = 50


def _rank_scores(terms: Sequence[str], top_n: int = TOP_N) -> dict[str, float]:
    """정렬된 키워드 목록을 50점부터 1점까지의 순위 점수로 바꿉니다."""
    # 첫 번째 키워드에는 top_n점, 마지막 키워드에는 1점을 부여합니다.
    return {term: float(top_n - index) for index, term in enumerate(terms[:top_n])}


def frequency_scores(video: dict[str, Any]) -> dict[str, float]:
    """제목·태그·댓글 출처별 가중치를 적용한 빈도 점수를 계산합니다."""
    # 각 키워드의 점수를 저장할 일반 딕셔너리를 만듭니다.
    scores: dict[str, float] = {}
    # 제목 후보마다 30점을 부여합니다.
    for term in video.get("title_nouns", []):
        scores[term] = TITLE_WEIGHT
    # 태그 후보마다 기존 점수에 10점을 더합니다.
    for term in video.get("tag_nouns", []):
        scores[term] = scores.get(term, 0.0) + TAG_WEIGHT
    # 댓글 후보가 등장할 때마다 0.1점씩 누적합니다.
    for term in video.get("comment_nouns", []):
        scores[term] = scores.get(term, 0.0) + COMMENT_WEIGHT
    # 출처별 가중치가 반영된 점수 사전을 반환합니다.
    return scores


def textrank_scores(
    tokens: Sequence[str],
    window_size: int = 4,
    top_n: int = TOP_N,
) -> dict[str, float]:
    """댓글 토큰의 동시 출현 그래프에서 중심적인 키워드를 점수화합니다."""
    # 필요한 시점에만 NetworkX를 불러와 모듈 자체의 가벼움을 유지합니다.
    import networkx as nx

    # 연결 관계를 만들 수 없는 짧은 입력은 빈 점수를 반환합니다.
    if len(tokens) < 2:
        return {}
    # 무방향 그래프를 생성합니다. 노드는 키워드, 간선은 동시 출현입니다.
    graph = nx.Graph()
    # 모든 고유 토큰을 그래프 노드로 등록합니다.
    graph.add_nodes_from(set(tokens))
    # 각 토큰을 기준으로 뒤쪽 윈도우 안의 토큰을 확인합니다.
    for index, term in enumerate(tokens):
        # window_size=4이면 현재 토큰과 최대 세 칸 뒤 토큰까지 연결합니다.
        for neighbor in tokens[index + 1 : index + window_size]:
            # 자기 자신과의 연결은 키워드 관계 정보가 없으므로 제외합니다.
            if term != neighbor:
                # 같은 쌍이 다시 등장하면 기존 간선 가중치에 1을 더합니다.
                weight = graph.get_edge_data(term, neighbor, {}).get("weight", 0) + 1
                # 계산한 가중치로 간선을 생성하거나 갱신합니다.
                graph.add_edge(term, neighbor, weight=weight)

    # 간선 가중치를 반영한 PageRank로 문맥 중심성을 계산합니다.
    ranks = nx.pagerank(graph, weight="weight")
    # PageRank 점수가 큰 순서대로 키워드만 추출합니다.
    ordered = [term for term, _ in sorted(ranks.items(), key=lambda item: item[1], reverse=True)]
    # 상위 키워드를 순위 점수로 변환해 반환합니다.
    return _rank_scores(ordered, top_n)


def tfidf_krwordrank_scores(
    videos: Sequence[dict[str, Any]],
    top_n: int = TOP_N,
) -> list[dict[str, float]]:
    """카테고리 댓글 코퍼스에서 TF-IDF와 KRWordRank를 결합합니다."""
    # 필요한 시점에만 NLP 라이브러리를 불러옵니다.
    import numpy as np
    from krwordrank.word import KRWordRank
    from sklearn.feature_extraction.text import TfidfVectorizer

    # 영상별 댓글 후보를 공백으로 이어 하나의 문서로 만듭니다.
    corpus = [" ".join(video.get("comment_nouns", [])) for video in videos]
    # 영상이 없거나 모든 댓글이 비어 있으면 계산할 수 없으므로 빈 점수를 반환합니다.
    if not corpus or not any(corpus):
        return [{} for _ in videos]

    # 같은 벡터라이저로 TF-IDF 행렬과 해당 열의 키워드 이름을 만듭니다.
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(corpus)
    feature_names = np.array(vectorizer.get_feature_names_out())
    # 카테고리 전체 코퍼스에서 KRWordRank 중요도를 계산합니다.
    wordrank, _, _ = KRWordRank(min_count=1, max_length=10).extract(
        corpus, beta=0.85, max_iter=10
    )

    # 영상별 TF-IDF/KRWordRank 결과를 순서대로 저장합니다.
    results: list[dict[str, float]] = []
    # TF-IDF 행렬의 각 행은 영상 하나의 댓글 문서에 대응합니다.
    for row in matrix:
        # TF-IDF가 0보다 큰 키워드만 골라 두 중요도의 곱을 계산합니다.
        importance = {
            feature_names[column]: value * wordrank.get(feature_names[column], 0.0)
            for column, value in enumerate(row.toarray().ravel())
            if value > 0
        }
        # 결합 중요도가 큰 순서대로 키워드를 정렬합니다.
        ordered = [term for term, _ in sorted(importance.items(), key=lambda item: item[1], reverse=True)]
        # 실제 곱 값 대신 순위 점수로 변환해 다른 점수와 스케일을 맞춥니다.
        results.append(_rank_scores(ordered, top_n))
    # 입력 영상 순서와 동일한 점수 목록을 반환합니다.
    return results


def score_category_videos(videos: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """같은 카테고리 영상들에 세 점수와 combined_score를 추가합니다."""
    # TF-IDF/KRWordRank는 카테고리 코퍼스 전체가 필요하므로 한 번에 계산합니다.
    corpus_scores = tfidf_krwordrank_scores(videos)
    # 점수화된 영상 레코드를 담을 리스트를 만듭니다.
    scored: list[dict[str, Any]] = []

    # 영상과 해당 영상의 코퍼스 점수를 같은 순서로 함께 순회합니다.
    for video, corpus_score in zip(videos, corpus_scores):
        # 원본 영상 딕셔너리를 보존하기 위해 복사본을 사용합니다.
        result = dict(video)
        # 제목·태그·댓글의 출처 가중치 점수를 저장합니다.
        result["frequency_score"] = frequency_scores(result)
        # 댓글 문맥의 중심성 점수를 저장합니다.
        result["textrank_score"] = textrank_scores(result.get("comment_nouns", []))
        # 카테고리 내 상대적 중요도 점수를 저장합니다.
        result["tfidf_krwordrank_score"] = corpus_score

        # 키워드가 어느 점수에만 등장해도 0부터 안전하게 누적하도록 defaultdict를 사용합니다.
        combined: defaultdict[str, float] = defaultdict(float)
        # 세 종류의 점수 사전을 차례로 합산합니다.
        for component in (
            result["frequency_score"],
            result["textrank_score"],
            result["tfidf_krwordrank_score"],
        ):
            # 현재 점수 사전의 모든 키워드와 점수를 순회합니다.
            for term, score in component.items():
                # 동일 키워드의 점수를 누적합니다.
                combined[term] += score
        # 합산 점수가 큰 순서로 정렬해 combined_score에 저장합니다.
        result["combined_score"] = dict(
            sorted(combined.items(), key=lambda item: item[1], reverse=True)
        )
        # 점수화가 끝난 영상을 결과 리스트에 추가합니다.
        scored.append(result)
    # 카테고리 내 모든 점수화 영상을 반환합니다.
    return scored
