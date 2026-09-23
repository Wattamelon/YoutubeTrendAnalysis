"""YouTube Trend Analysis의 핵심 분석 모듈 패키지입니다.

이 패키지는 원본 서비스에서 API, 데이터베이스, 프런트엔드 코드를 분리하고
면접에서 설명할 데이터 분석 로직만 독립적으로 정리한 영역입니다.

전체 처리 흐름은 다음과 같습니다.

    preprocessing  → 댓글 노이즈 제거·표현 정규화
    tokenization    → Kiwi 형태소 분석으로 키워드 후보 추출
    keyword_scoring → 빈도·TextRank·TF-IDF/KRWordRank 점수 결합
    ranking         → 기간별 키워드 집계와 이전 순위 비교
    related_keywords→ N-gram·PMI 기반 연관 키워드 산출

각 모듈은 외부 API와 MongoDB에 직접 연결하지 않습니다. 따라서 작은 입력
데이터만으로도 개별 알고리즘을 검증하고 설명할 수 있습니다.
"""
