# related_ngram_runner.py
import sys
import json
from related_ngram_pmi import related_keyword_video_level
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if __name__ == "__main__":
    keyword = sys.argv[1]
    result = related_keyword_video_level(keyword)
    print(json.dumps(result, ensure_ascii=False, default=str))
