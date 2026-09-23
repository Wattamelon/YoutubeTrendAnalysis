from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
from krwordrank.word import KRWordRank
from collections import defaultdict
from datetime import datetime
import numpy as np

def tfidf_krrank(videos, top_n=10):
    
    # 해당 카테고리의 모든 동영상에 대해 코퍼스 구성
    corpus = []
    for video in videos:
        nouns = video.get("comments_nouns", [])
        doc = " ".join(nouns)
        corpus.append(doc)
    
    # 해당 카테고리 코퍼스에 대해 TF-IDF 계산
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    feature_names = np.array(vectorizer.get_feature_names_out())
        
    # 해당 카테고리 코퍼스에 대해 KRWordRank 계산
    beta = 0.85
    max_iter = 10
    wordrank_extractor = KRWordRank(min_count=1, max_length=10)
    krrank_scores, _, _ = wordrank_extractor.extract(corpus, beta, max_iter)
        
    # 각 동영상별로 TF-IDF와 KRWordRank 점수를 결합하여 키워드 추출
    for idx, video in enumerate(videos):
        doc_vector = tfidf_matrix[idx].toarray().flatten()
        combined_scores = {}
        for j, tfidf_val in enumerate(doc_vector):
            if tfidf_val > 0:
                word = feature_names[j]
                # KRWordRank 점수가 없으면 0 사용
                krrank_val = krrank_scores.get(word, 0)
                combined_score = tfidf_val * krrank_val
                combined_scores[word] = combined_score
        # 결합 점수 내림차순 정렬 후 상위 top_n 단어 추출
        sorted_words = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        top_keywords = [word for word, score in sorted_words[:top_n]]
        video["tf_keywords"] = top_keywords

    print("✅ 카테고리별 TF-IDF와 KRWordRank 기반 키워드 추출 완료!")
    return videos


def textrank_keywords(tokens, window_size=4, top_n=10):
    """
    주어진 토큰 리스트에 대해 TextRank 알고리즘을 적용해 키워드를 추출합니다.
    
    Parameters:
      tokens (list of str): 명사 토큰 리스트
      window_size (int): 단어 간 연결을 위한 윈도우 크기
      top_n (int): 상위 몇 개 단어를 키워드로 추출할지 결정
      
    Returns:
      list: 상위 top_n 키워드 리스트
    """
    if not tokens:
        return []
    
    # 그래프 생성: 노드는 토큰, 엣지는 윈도우 내 단어 쌍
    graph = nx.Graph()
    graph.add_nodes_from(set(tokens))
    
    for i in range(len(tokens)):
        for j in range(i+1, min(i+window_size, len(tokens))):
            if tokens[i] != tokens[j]:
                if graph.has_edge(tokens[i], tokens[j]):
                    graph[tokens[i]][tokens[j]]['weight'] += 1
                else:
                    graph.add_edge(tokens[i], tokens[j], weight=1)
    
    # PageRank 적용
    ranks = nx.pagerank(graph, weight='weight')
    # 점수 내림차순 정렬 후 상위 top_n 단어 추출
    sorted_tokens = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [word for word, score in sorted_tokens[:top_n]]
    return top_keywords

def score_video_keywords(data):
    
    for category, videos in data.items():
        # 빈도수 기반 score
        for video in videos:
            keywords_scores = {}
            # 제목
            title_nouns = video.get("title_nouns", [])
            for noun in title_nouns:
                keywords_scores[noun] = 30
            # tag
            tag_nouns = video.get("tag_nouns", [])
            for noun in tag_nouns:
                if noun not in keywords_scores:
                    keywords_scores[noun] = 10
                else:
                    keywords_scores[noun] += 10  
            # comments
            comments_nouns = video.get("comments_nouns", [])
            for noun in comments_nouns:
                if noun not in keywords_scores:
                    keywords_scores[noun] = 0.1
                
                else:
                    keywords_scores[noun] += 0.1
            video["freq_score"] = keywords_scores
        
        # textrank 기반 score    
        for video in videos:
            krrank_keywords_scores = {}
            
            comments_nouns = video.get("comments_nouns", [])
            keywords = textrank_keywords(comments_nouns, top_n = 50)
            
            for i, keyword in enumerate(keywords):
                krrank_keywords_scores[keyword] = 50 - i
            
            video["text_score"] = krrank_keywords_scores
    
        
        #tf_idf_krrank 기반 score
        tf_idf_videos = tfidf_krrank(videos, top_n=50)
        
        for idx, video in enumerate(videos):
            tf_kr_keywords_scores = {}
            tf_keywords = tf_idf_videos[idx].get("tf_keywords", [])     # tf의 키워드 리스트트
            for i, keyword in enumerate(tf_keywords):
                tf_kr_keywords_scores[keyword] = 50 - i
            video["tf_kr_score"] = tf_kr_keywords_scores
        
    return data

def extract_category_keywords(data, top_n=100):

    category_keywords = {}

    for category, videos in data.items():
        # 카테고리 내 모든 동영상의 combined_score를 누적할 딕셔너리
        accumulated_scores = {}
        
        for video in videos:
            # 동영상의 인기 점수 (예: 조회수 + 10*좋아요 + 5*댓글수)
            popularity = video.get("view_count", 0) + video.get("like_count", 0)*10 + video.get("comment_count", 0)*5
            combined_score = video.get("combined_score", {})
            # 각 키워드에 대해 popularity 가중치 곱한 값을 누적
            for keyword, score in combined_score.items():
                weighted_score = score * popularity
                accumulated_scores[keyword] = accumulated_scores.get(keyword, 0) + weighted_score
        
        # 누적된 점수를 내림차순 정렬하여 상위 top_n 키워드 선택
        sorted_keywords = sorted(accumulated_scores.items(), key=lambda x: x[1], reverse=True)
        top_category_keywords = [kw for kw, s in sorted_keywords[:top_n]]
        category_keywords[category] = top_category_keywords

    return category_keywords

def combine_keyword_scores(video, weights=None):
    """
    freq_score, text_score, tf_kr_score를 통합하여 combined_score 생성
    Parameters:
        video (dict): 영상 하나의 정보
        weights (dict): 각 스코어의 가중치 (기본값은 동일한 비율)
            예시: {'freq': 1.0, 'text': 1.5, 'tf_kr': 2.0}
    Returns:
        dict: combined_score 딕셔너리
    """
    freq = video.get("freq_score", {})
    text = video.get("text_score", {})
    tfkr = video.get("tf_kr_score", {})

    combined = defaultdict(float)

    # 기본 가중치 설정
    if weights is None:
        weights = {"freq": 1.0, "text": 1.0, "tf_kr": 1.0}

    for word, score in freq.items():
        combined[word] += score * weights.get("freq", 1.0)
    for word, score in text.items():
        combined[word] += score * weights.get("text", 1.0)
    for word, score in tfkr.items():
        combined[word] += score * weights.get("tf_kr", 1.0)

    return dict(combined)


def apply_combined_scores(data, weights=None):
    """
    전체 데이터에 대해 combined_score 계산 후 video["combined_score"]에 저장
    Parameters:
        data (dict): 카테고리별 영상 데이터
        weights (dict): 각 점수의 가중치 (선택)
    Returns:
        dict: combined_score가 포함된 원본 데이터
    """
    for category, videos in data.items():
        for video in videos:
            video["combined_score"] = combine_keyword_scores(video, weights)
    return data
