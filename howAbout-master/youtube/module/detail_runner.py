# analyze_keyword_runner.py
import sys
import json
from keyword_detail import analyze_keyword_success  # 아래 함수는 별도 모듈로 분리된 경우

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "❌ 키워드를 인자로 전달해주세요 (예: python analyze_keyword_runner.py BTS)"}), flush=True)
        sys.exit(1)

    keyword = sys.argv[1]
    result = analyze_keyword_success(keyword)
    print(result)  # 이미 JSON 형식으로 출력됨
