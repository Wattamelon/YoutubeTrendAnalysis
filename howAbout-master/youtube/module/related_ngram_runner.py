# related_ngram_runner.py
import sys
import json
from related_ngram_pmi import related_ngram_pmi

if __name__ == "__main__":
    keyword = sys.argv[1]
    result = related_ngram_pmi(keyword)
    print(json.dumps(result, ensure_ascii=False))
