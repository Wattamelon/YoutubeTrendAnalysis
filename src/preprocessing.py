"""댓글 텍스트 정제와 카테고리별 표현 정규화 모듈입니다.

이 모듈은 분석 파이프라인의 첫 단계입니다. YouTube 댓글에는 HTML 태그,
URL, 이모지, 대소문자 차이, 별칭, 오탈자가 함께 섞여 있습니다. 이런 원문을
그대로 형태소 분석하면 같은 대상을 여러 키워드로 잘못 세거나 의미 없는
웹 요소가 키워드 후보가 될 수 있습니다.

입력:
    text     - 댓글 원문 문자열
    category - 영상 카테고리. 카테고리별 별칭 사전을 선택하는 데 사용

출력:
    정제된 문자열. 이후 tokenization 모듈이 이 문자열을 형태소 분석합니다.

핵심 처리:
    1. HTML, URL, HTML entity, 이모지를 제거합니다.
    2. 영문을 소문자로 통일합니다.
    3. 예를 들어 BTS와 방탄소년단처럼 같은 대상을 가리키는 표현을
       카테고리별 대표 키워드 하나로 통일합니다.
    4. 연속 공백을 정리합니다.

별칭 사전은 규칙 기반 전처리의 예시입니다. 실제 서비스에서는 분석 결과와
새로운 유행어를 바탕으로 사전을 지속적으로 보완하는 것을 전제로 합니다.
"""

from __future__ import annotations  # 최신 타입 표기법을 안전하게 사용합니다.

import re  # 정규표현식 기반 텍스트 치환에 사용합니다.
from collections.abc import Mapping  # 별칭 사전의 추상 타입을 표현합니다.

# 카테고리별로 자주 등장하는 별칭을 대표 표현으로 통일합니다.
# 실제 서비스에서는 이 사전을 데이터와 함께 계속 확장할 수 있습니다.
DEFAULT_ALIASES: dict[str, dict[str, str]] = {
    "News & Politics": {
        "윤대통령": "윤석열",
        "윤석렬": "윤석열",
        "국힘": "국민의힘",
        "국짐": "국민의힘",
        "대통령 선거": "대선",
        "특별검사": "특검",
    },
    "Music": {
        "bts": "방탄소년단",
        "블핑": "블랙핑크",
        "blackpink": "블랙핑크",
        "newjeans": "뉴진스",
        "njz": "뉴진스",
        "gd": "지드래곤",
    },
}


def normalize_aliases(
    text: str,
    category: str,
    aliases: Mapping[str, Mapping[str, str]] = DEFAULT_ALIASES,
) -> str:
    """동일 대상을 가리키는 표현을 하나의 대표 키워드로 바꿉니다."""
    # 현재 카테고리에 등록된 별칭만 꺼내 반복합니다.
    for variant, canonical in aliases.get(category, {}).items():
        # re.escape로 특수문자가 포함된 별칭도 안전하게 검색합니다.
        # IGNORECASE로 영문 별칭의 대소문자 차이를 제거합니다.
        text = re.sub(re.escape(variant), canonical, text, flags=re.IGNORECASE)
    # 정규화된 텍스트를 반환합니다.
    return text


def clean_comment(text: str, category: str) -> str:
    """웹·댓글 노이즈를 제거하고 키워드 분석용 텍스트를 반환합니다."""
    # HTML 태그를 공백으로 바꿔 문장에 붙어 있던 단어를 분리합니다.
    text = re.sub(r"<[^>]+>", " ", text)
    # 자주 수집되는 HTML entity를 일반 공백으로 바꿉니다.
    text = text.replace("&quot", " ").replace("&lt", " ").replace("&gt", " ")
    # URL, 멘션, 해시태그 기호처럼 의미가 약한 웹 요소를 제거합니다.
    text = re.sub(r"https?://\S+|www\.\S+|@\S+|#", " ", text)
    # 확장 유니코드 범위의 이모지를 제거합니다.
    text = re.sub(r"[\U00010000-\U0010ffff]", " ", text)
    # 영문 대소문자를 통일한 후 카테고리별 별칭을 정규화합니다.
    text = normalize_aliases(text.lower(), category)
    # 연속 공백을 하나로 줄이고 양 끝 공백을 제거해 반환합니다.
    return re.sub(r"\s+", " ", text).strip()
