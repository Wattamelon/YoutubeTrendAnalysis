# resolve_keywords.py
import sys
import json
from related_ngram_pmi import related_keyword_video_level  # 위에서 만든 함수 import

if __name__ == "__main__":
    keyword = sys.argv[1]
    result = related_keyword_video_level(keyword)
    print(json.dumps(result, ensure_ascii=False))
