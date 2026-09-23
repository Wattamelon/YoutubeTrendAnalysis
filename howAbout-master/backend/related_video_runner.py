# related_ngram_runner.py
import sys
import json
from related_video import fetch_most_related_videos_by_keyword

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if __name__ == "__main__":
    keyword = sys.argv[1]
    result = fetch_most_related_videos_by_keyword(keyword)
    print(json.dumps(result, ensure_ascii=False, default=str))
