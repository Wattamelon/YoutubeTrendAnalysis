import re
import emoji
from init import *
import time
import datetime
import isodate
import os
CATEGORIES = {
    "News & Politics": "25",
    'Music' : "10",
    'Sports' : "17",
    'Gaming' : "20",
    'Science & Technology': "28"
}

# 텍스트 데이터를 전처리하는 함수
def clean_text(text, category):
    
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', ' ', text)
    # &quot 제거
    text = text.replace("&quot", " ")
    text = text.replace("&lt", " ")
    text = text.replace("&gt", " ")
    # URL, 멘션, 해시태그 제거
    text = re.sub(r'http\S+|www\S+|@+|#', " ", text)
    # 한글, 영어, 숫자, 공백을 제외한 모든 문자 제거

   
    # 앞뒤 공백 제거
    text = text.strip()
    # 모든 이모지 제거
    text = emoji.replace_emoji(text, replace=" ")
    # 영어를 소문자로 변환
    
    text = text.lower()
    
    if category == "News & Politics":
        text = re.sub(r"채널A|channelA", "채널A", text)
        text = re.sub(r"대한민국", "한국", text)
        text = re.sub(r"윤대통령|윤대통|윤통|윤석렬|윤썩렬|윤씨", "윤석열", text)
        text = re.sub(r"(?<!윤)석열", "윤석열", text)
        text = re.sub(r"국힘|국민의힘당|국짐|국민의 짐", "국민의힘", text)
        text = re.sub(r"이재명|이잼명|이잼", "이재명", text)
        text = re.sub(r"한동훈|한뚜기|한장관", "한동훈", text)
        text = re.sub(r"조국|조로남불석", "조국", text)
        text = re.sub(r"김건희|김여사|건희사랑|김거니", "김건희", text)
        text = re.sub(r"(?<!김)건희", "김건희", text)
        text = re.sub(r"(?<!김)거니", "김건희", text)
        text = re.sub(r"나경원|나베", "나경원", text)
        text = re.sub(r"문재인|달님|문프", "문재인", text)
        text = re.sub(r"박근혜|503", "박근혜", text)
        text = re.sub(r"이명박|mb", "이명박", text)
        text = re.sub(r"검찰공화국|검찰쿠데타", "검찰", text)
        text = re.sub(r"윤핵관", "윤핵관", text)
        text = re.sub(r"이낙연|이낙연계", "이낙연", text)
        text = re.sub(r"홍준표|홍카콜라", "홍준표", text)
        text = re.sub(r"추미애|추장관", "추미애", text)
        text = re.sub(r"심상정|심블리", "심상정", text)
        text = re.sub(r"이준석|준스톤", "이준석", text)
        text = re.sub(r"(?<!이)준석", "이준석", text)
        text = re.sub(r"강경보수", "보수", text)
        text = re.sub(r"강경진보", "진보", text)
        text = re.sub(r"메가시티", "광역도시", text)
        text = re.sub(r"청와대|대통령실", "대통령실", text)
        text = re.sub(r"국정원|국가정보원", "국가정보원", text)
        text = re.sub(r"공수처|고위공직자범죄수사처", "고위공직자범죄수사처", text)
        text = re.sub(r"특검|특별검사", "특검", text)
        text = re.sub(r"검찰개혁", "검찰개혁", text)
        text = re.sub(r"법무부", "법무부", text)
        text = re.sub(r"대법원", "대법원", text)
        text = re.sub(r"헌법재판소|헌재", "헌법재판소", text)
        text = re.sub(r"국회의원|국개의원", "국회의원", text)
        text = re.sub(r"대선|대통령 선거", "대통령 선거", text)
        text = re.sub(r"총선|국회의원 선거", "국회의원 선거", text)
        text = re.sub(r"지방선거", "지방선거", text)
        text = re.sub(r"한미동맹|한미관계", "한미동맹", text)
        text = re.sub(r"북핵|북한 핵무기", "북핵", text)
        text = re.sub(r"중국 경제", "중국경제", text)
        text = re.sub(r"일본 경제", "일본경제", text)
        text = re.sub(r"대북제재", "대북제재", text)
        text = re.sub(r"종전선언", "종전선언", text)
        text = re.sub(r"군사협력", "군사협력", text)
        text = re.sub(r"정전협정", "정전협정", text)
        text = re.sub(r"공무원연금개혁", "공무원연금개혁", text)
        text = re.sub(r"노동개혁", "노동개혁", text)
        text = re.sub(r"연금개혁", "연금개혁", text)
        text = re.sub(r"부동산정책", "부동산정책", text)
        text = re.sub(r"전월세", "전월세", text)
        text = re.sub(r"기본소득", "기본소득", text)
        text = re.sub(r"최저임금", "최저임금", text)
        text = re.sub(r"비정규직", "비정규직", text)
        text = re.sub(r"경제성장률", "경제성장률", text)
        text = re.sub(r"국가채무", "국가채무", text)
        text = re.sub(r"무역적자", "무역적자", text)
        text = re.sub(r"외환보유액", "외환보유액", text)
        text = re.sub(r"코스피", "코스피", text)
        text = re.sub(r"코스닥", "코스닥", text)
        text = re.sub(r"금리인상", "금리인상", text)
        text = re.sub(r"물가상승률", "물가상승률", text)
        text = re.sub(r"중소기업지원", "중소기업지원", text)
        text = re.sub(r"대기업규제", "대기업규제", text)
        text = re.sub(r"벤처기업", "벤처기업", text)
    elif category == "Music":
        text = re.sub(r"방탄소년단|bts", "방탄소년단", text)
        text = re.sub(r"\b방탄\b(?! 소년단)", "방탄소년단", text) # 방탄 뒤에 소년단이 없으면 방탄소년단으로 변환
        text = re.sub(r"블랙핑크|blackpink|블핑", "블랙핑크", text)
        text = re.sub(r"르세라핌|lesserafim", "르세라핌", text)
        text = re.sub(r"뉴진스|newjeans|njz", "뉴진스", text)
        text = re.sub(r"아이브|ive", "아이브", text)
        text = re.sub(r"세븐틴|svt", "세븐틴", text)
        text = re.sub(r"엔시티|nct|n시티", "엔시티", text)
        text = re.sub(r"스트레이키즈|스키즈|stray kids|straykids", "스트레이키즈", text)
        text = re.sub(r"에스파|aespa", "에스파", text)
        text = re.sub(r"지드래곤|gd|권지용|지디|g-dragon", "지드래곤", text)
        text = re.sub(r"태양|동영배", "태양", text)
        text = re.sub(r"트와이스|twice", "트와이스", text)
        text = re.sub(r"아이유|iu", "아이유", text)
        text = re.sub(r"제로베이스원|zb1|제베", "제로베이스원", text)
        text = re.sub(r"보이넥스트도어|boynextdoor|보넥도", "보이넥스트도어", text)
        text = re.sub(r"투모로우바이투게더|txt|투바투", "투모로우바이투게더", text)
        text = re.sub(r"지민|박지민", "지민", text)
        text = re.sub(r"뷔|김태형|태형", "뷔", text)
        text = re.sub(r"정국|전정국", "정국", text)
        text = re.sub(r"슈가|민윤기", "슈가", text)
        text = re.sub(r"rm|김남준|남준", "rm", text)
        text = re.sub(r"제이홉|j-hope|정호석", "제이홉", text)
        text = re.sub(r"엑소|exo", "엑소", text)
        text = re.sub(r"갓세븐|got7", "갓세븐", text)
        text = re.sub(r"레드벨벳|red velvet|redvelvet", "레드벨벳", text)
        text = re.sub(r"오마이걸|oh my girl|ohmygirl|옴걸", "오마이걸", text)
        text = re.sub(r"하이브|hybe", "하이브", text)
        text = re.sub(r"\bsm\b(?! 엔터테이먼트)", "sm엔터테이먼트", text) 
        text = re.sub(r"\byg\b(?! 엔터테이먼트)", "yg엔터테이먼트", text) 
        text = re.sub(r"\bjyp\b(?! 엔터테이먼트)", "jyp엔터테이먼트", text) 
        text = re.sub(r"빅히트|bighit", "하이브", text)
        text = re.sub(r"에이티즈|ateez", "에이티즈", text)
        text = re.sub(r"더보이즈|the boyz", "더보이즈", text)
        text = re.sub(r"스테이씨|stayc", "스테이씨", text)
        text = re.sub(r"엔하이픈|enhypen", "엔하이픈", text)
        text = re.sub(r"케플러|kep1er", "케플러", text)
        text = re.sub(r"위클리|weeekly", "위클리", text)
        text = re.sub(r"트레저|treasure", "트레저", text)
        text = re.sub(r"에버글로우|everglow", "에버글로우", text)
        text = re.sub(r"비투비|btob", "비투비", text)
        text = re.sub(r"몬스타엑스|monsta x|몬엑", "몬스타엑스", text)
        text = re.sub(r"sf9", "sf9", text)
        text = re.sub(r"베리베리|verivery", "베리베리", text)
        text = re.sub(r"골든차일드|golden child|goldenchild", "골든차일드", text)
        text = re.sub(r"펜타곤|pentagon", "펜타곤", text)
        text = re.sub(r"체리블렛|cherry bullet", "체리블렛", text)
        text = re.sub(r"크래비티|cravity", "크래비티", text)
        text = re.sub(r"씨아이엑스|cix", "씨아이엑스", text)
        text = re.sub(r"온앤오프|onf", "온앤오프", text)
        text = re.sub(r"원어스|oneus", "원어스", text)
        text = re.sub(r"드림캐쳐|dreamcatcher", "드림캐쳐", text)
        text = re.sub(r"시크릿넘버|secret number", "시크릿넘버", text)
        text = re.sub(r"라붐|laboum", "라붐", text)
        text = re.sub(r"마마무|mamamoo", "마마무", text)
        text = re.sub(r"브레이브걸스|brave girls|쁘쁘걸", "브레이브걸스", text)
        text = re.sub(r"에이핑크|apink", "에이핑크", text)
        text = re.sub(r"씨스타|sistar", "씨스타", text)
        text = re.sub(r"카라|kara", "카라", text)
        text = re.sub(r"소녀시대|snsd|소시", "소녀시대", text)
        text = re.sub(r"슈퍼주니어|super junior", "슈퍼주니어", text)
        text = re.sub(r"빅뱅|bigbang", "빅뱅", text)
        text = re.sub(r"원더걸스|wonder girls", "원더걸스", text)
        text = re.sub(r"2ne1|투애니원|투에니원", "2ne1", text)
        text = re.sub(r"샤이니|shinee", "샤이니", text)
        text = re.sub(r"인피니트|infinite", "인피니트", text)
        text = re.sub(r"비스트|beast|하이라이트|highlight", "하이라이트", text)
        text = re.sub(r"틴탑|teen top|teentop", "틴탑", text)
        text = re.sub(r"엠블랙|mblaq", "엠블랙", text)
        text = re.sub(r"블락비|block b", "블락비", text)
        text = re.sub(r"제국의아이들|ze:a|제아", "제국의아이들", text)
        text = re.sub(r"t-ara", "티아라", text)
        text = re.sub(r"4minute", "포미닛", text)
        text = re.sub(r"jennie", "제니", text)
        text = re.sub(r"방탄소년단|bts", "방탄소년단", text)
        text = re.sub(r"\b방탄\b(?!\s*소년단)", "방탄소년단", text)
        text = re.sub(r"블랙핑크|blackpink|블핑", "블랙핑크", text)
        text = re.sub(r"엑소|exo", "엑소", text)
        text = re.sub(r"트와이스|twice", "트와이스", text)
        text = re.sub(r"레드벨벳|red\s*velvet", "레드벨벳", text)
        text = re.sub(r"엔시티|nct", "엔시티", text)
        text = re.sub(r"갓세븐|got7", "갓세븐", text)
        text = re.sub(r"몬스타\s*엑스|monsta\s*x", "몬스타엑스", text)
        text = re.sub(r"세븐틴|seventeen", "세븐틴", text)
        text = re.sub(r"있지|itzy", "있지", text)
        text = re.sub(r"에이티즈|ateez", "에이티즈", text)
        text = re.sub(r"txt", "txt", text)
        text = re.sub(r"엔하이픈|enhypen", "엔하이픈", text)
        text = re.sub(r"스트레이\s*키즈|stray\s*kids", "스트레이 키즈", text)
        text = re.sub(r"아이브|ive", "아이브", text)
        text = re.sub(r"르세라핌|lesserafim", "르세라핌", text)
        text = re.sub(r"뉴진스|newjeans|njz", "뉴진스", text)
        text = re.sub(r"\(g\)idle|gidle", "아이들", text)
        text = re.sub(r"소녀시대|girls'? generation", "소녀시대", text)
        text = re.sub(r"카라", "카라", text)
        text = re.sub(r"원더걸스|wonder girls", "원더걸스", text)
        text = re.sub(r"미쓰에이|miss a", "미쓰에이", text)
        text = re.sub(r"티아라|t-ara", "티아라", text)
        text = re.sub(r"애프터스쿨|after school", "애프터스쿨", text)
        text = re.sub(r"레인보우|rainbow", "레인보우", text)
        text = re.sub(r"포미닛|4minute", "포미닛", text)
        text = re.sub(r"sistar", "씨스타", text)
        text = re.sub(r"apink", "에이핑크", text)
        text = re.sub(r"lovelyz", "러블리즈", text)
        text = re.sub(r"izone|iz\*one", "아이즈원", text)
        text = re.sub(r"fromis_9", "프로미스나인", text)
        text = re.sub(r"wjsn|cosmic\s*girls", "우주소녀", text)
        text = re.sub(r"loona", "루나", text)
        text = re.sub(r"clc", "씨엘씨", text)
        text = re.sub(r"april", "에이프릴", text)
        text = re.sub(r"pristin", "프리스틴", text)
        text = re.sub(r"bestie", "베스티", text)
        text = re.sub(r"spica", "스파이카", text)
        text = re.sub(r"btob", "비투비", text)
        text = re.sub(r"highlight", "하이라이트", text)
        text = re.sub(r"sechs\s*kies", "젝스키스", text)
        text = re.sub(r"gugudan", "구구단", text)
        text = re.sub(r"busters", "버스터즈", text)
        text = re.sub(r"berry\s*good", "베리굿", text)
        text = re.sub(r"hello\s*venus", "헬로비너스", text)
        
        # K-pop 대표 솔로 가수 및 멤버
        text = re.sub(r"boa", "보아", text)
        text = re.sub(r"lee\s*hyori", "이효리", text)
        text = re.sub(r"iu", "아이유", text)
        text = re.sub(r"taeyeon", "태연", text)
        text = re.sub(r"hyuna", "현아", text)
        text = re.sub(r"sunmi", "선미", text)
        text = re.sub(r"soyeon", "소연", text)
        text = re.sub(r"mamamoo", "마마무", text)
        text = re.sub(r"brown\s*eyed\s*girls", "브라운 아이드 걸스", text)
        text = re.sub(r"akmu", "악뮤", text)
    elif category == "Sports":
        #축구 관련 키워드
        text = re.sub(r"손흥민|son|쏘니|소니|sonny|느그흥|손세이셔널|대흥민|축신흥|소닉|캡틴손|캡틴 손|슈퍼손|소농민|흥미니|손흥민선수|흥민선수", "손흥민", text)
        text = re.sub(r"(?<!손)흥민", "손흥민", text) #흥민 앞에 손이 없으면 손흥민으로 변환
        text = re.sub(r"이강인|칸진리|강인이", "이강인", text)
        text = re.sub(r"김민재|괴물수비수|찐민짜이", "김민재", text)
        text = re.sub(r"(?<!김)민재", "김민재", text)
        text = re.sub(r"메시|리오넬 메시|메좆", "메시", text)
        text = re.sub(r"호날두|크리스티아누 호날두|좆두|호좆두", "호날두", text)
        text = re.sub(r"박지성|두개의심장|지성팍|박지성선수", "박지성", text)
        text = re.sub(r"황희찬|황소|희찬선수|희차니|희찬이형", "황희찬", text)
        text = re.sub(r"정우영|작우영|큰우영", "정우영", text)
        text = re.sub(r"손흥민 골|손흥민 득점", "손흥민 골", text)
        text = re.sub(r"맨유|맨체스터 유나이티드|맹구", "맨체스터 유나이티드", text)
        text = re.sub(r"맨시티|맨체스터 시티", "맨체스터 시티", text)
        text = re.sub(r"리버풀", "리버풀", text)
        text = re.sub(r"첼시", "첼시", text)
        text = re.sub(r"아스톤빌라|아스톤 빌라|av", "아스톤빌라", text)
        text = re.sub(r"아스날|개스날|사스날", "아스날", text)
        text = re.sub(r"토트넘|스퍼스|닭집", "토트넘", text)
        text = re.sub(r"모하메드 살라|모하메드살라|살라", "살라", text)
        text = re.sub(r"레알 마드리드", "레알 마드리드", text)
        text = re.sub(r"\b레알\b(?! 마드리드)", "레알 마드리드", text) #레알 뒤에 마드리드가 없으면 레알 마드리드로 변환
        text = re.sub(r"바르셀로나|바르사|바르샤", "바르셀로나", text)
        text = re.sub(r"바이에른 뮌헨|뮌헨", "바이에른 뮌헨", text)
        text = re.sub(r"(?<!바이에른)뮌헨", "바이에른 뮌헨", text) 
        text = re.sub(r"도르트문트|돌문|꿀벌", "도르트문트", text)
        text = re.sub(r"유벤투스|유베|유벤", "유벤투스", text)
        text = re.sub(r"ac 밀란", "ac 밀란", text)
        text = re.sub(r"인터 밀란", "인터 밀란", text)
        text = re.sub(r"psg|파리 생제르맹|파리 생제르망", "파리 생제르맹", text)
        text = re.sub(r"라리가", "라리가", text)
        text = re.sub(r"분데스리가|분데스리그", "분데스리가", text)
        text = re.sub(r"\b분데스\b(?! 리가)", "분데스리가", text)
        text = re.sub(r"\b분데스\b(?! 리그)", "분데스리가", text)
        text = re.sub(r"세리에a|세리에", "세리에", text)
        text = re.sub(r"리그앙", "리그앙", text)
        text = re.sub(r"k리그|k리그1|k리그2", "k리그", text)
        text = re.sub(r"챔스|uefa 챔피언스리그|챔피언스리그|ucl", "챔피언스리그", text)
        text = re.sub(r"유로파리그|유로파", "유로파리그", text)
        text = re.sub(r"아시안컵", "아시안컵", text)
        text = re.sub(r"월드컵|월컵", "월드컵", text)
        text = re.sub(r"코파아메리카|코파", "코파아메리카", text)
        text = re.sub(r"골든볼", "골든볼", text)
        text = re.sub(r"발롱도르|발롱", "발롱도르", text)
        text = re.sub(r"올림픽", "올림픽", text)
        text = re.sub(r"아시안게임", "아시안게임", text)
        
        # 야구 관련 키워드
        text = re.sub(r"류현진|ryu", "류현진", text)
        text = re.sub(r"김광현|kk", "김광현", text)
        text = re.sub(r"이정후", "이정후", text)
        text = re.sub(r"박병호", "박병호", text)
        text = re.sub(r"강백호", "강백호", text)
        text = re.sub(r"최지만", "최지만", text)
        text = re.sub(r"김하성", "김하성", text)
        text = re.sub(r"고우석", "고우석", text)
        text = re.sub(r"정우영", "정우영", text)
        text = re.sub(r"양현종", "양현종", text)
        text = re.sub(r"오타니|쇼헤이|ohtani", "오타니 쇼헤이", text)
        text = re.sub(r"다르빗슈", "다르빗슈 유", text)
        text = re.sub(r"wbc", "wbc", text)
        text = re.sub(r"mlb", "mlb", text)
        text = re.sub(r"npb", "npb", text)
        text = re.sub(r"kbo", "kbo", text)
        text = re.sub(r"삼성 라이온즈", "삼성 라이온즈", text)
        text = re.sub(r"롯데 자이언츠", "롯데 자이언츠", text)
        text = re.sub(r"두산 베어스", "두산 베어스", text)
        text = re.sub(r"lg 트윈스", "lg 트윈스", text)
        text = re.sub(r"키움 히어로즈", "키움 히어로즈", text)
        text = re.sub(r"kt 위즈", "kt 위즈", text)
        text = re.sub(r"한화 이글스", "한화 이글스", text)
        text = re.sub(r"ssg 랜더스", "ssg 랜더스", text)
        text = re.sub(r"nc 다이노스", "nc 다이노스", text)
        text = re.sub(r"홈런", "홈런", text)
        text = re.sub(r"타점", "타점", text)
        text = re.sub(r"득점", "득점", text)
        text = re.sub(r"방어율", "방어율", text)
        text = re.sub(r"출루율", "출루율", text)
        text = re.sub(r"타율", "타율", text)
        text = re.sub(r"골든글러브", "골든글러브", text)
        text = re.sub(r"사이영상", "사이영상", text)
        text = re.sub(r"메이저리그", "메이저리그", text)
        
        # 농구 관련 키워드
        text = re.sub(r"nba|느바", "nba", text)
        text = re.sub(r"wnba", "wnba", text)
        text = re.sub(r"르브론 제임스|르브론|릅신|릅갈|릅탄", "르브론 제임스", text)
        text = re.sub(r"스테판 커리|커리|스테픈 커리", "커리", text)
        text = re.sub(r"케빈 듀란트|듀란트", "듀란트", text)
        text = re.sub(r"야니스 아데토쿤보|야니스", "아데토쿤보", text)
        text = re.sub(r"루카 돈치치|돈치치|루카돈치치", "돈치치", text)
        text = re.sub(r"조엘 엠비드|엠비드", "엠비드", text)
        text = re.sub(r"니콜라 요키치|요키치", "요키치", text)
        text = re.sub(r"앤서니 데이비스|ad", "앤서니 데이비스", text)
        text = re.sub(r"데빈 부커|부커|데빈부커", "부커", text)
        text = re.sub(r"제이슨 테이텀|테이텀", "테이텀", text)
        text = re.sub(r"자 모란트|모란트", "모란트", text)
        text = re.sub(r"카이리 어빙|어빙", "어빙", text)
        text = re.sub(r"제임스 하든|하든", "하든", text)
        text = re.sub(r"클레이 탐슨|탐슨|클탐", "탐슨", text)
        text = re.sub(r"드레이먼드 그린|드레이먼드", "그린", text)
        text = re.sub(r"웸반야마|웸비", "웸반야마", text)
        text = re.sub(r"ncaa", "ncaa", text)
        text = re.sub(r"fiba", "fiba", text)
        text = re.sub(r"3점슛", "3점슛", text)
        text = re.sub(r"덩크슛", "덩크", text)
        text = re.sub(r"어시스트", "어시스트", text)
        text = re.sub(r"리바운드", "리바운드", text)
        text = re.sub(r"블록슛", "블록", text)
        text = re.sub(r"kbl|크블", "kbl", text)
    elif category == "Gaming":
        text = re.sub(r"리그오브레전드|lol|롤", "리그오브레전드", text)
        text = re.sub(r"배틀그라운드|pubg|배그|베그", "배틀그라운드", text)
        text = re.sub(r"발로란트|valorant", "발로란트", text)
        text = re.sub(r"오버워치|overwatch|옵치", "오버워치", text)
        text = re.sub(r"카트라이더|카트|kart", "카트라이더", text)
        text = re.sub(r"스타크래프트|스타1|스타2", "스타크래프트", text)
        text = re.sub(r"\b카트\b(?! 라이더)", "카트라이더", text)
        text = re.sub(r"\b스타\b(?! 크래프트)", "스타크래프트", text)
        text = re.sub(r"마인크래프트|마크|minecraft", "마인크래프트", text)
        text = re.sub(r"포켓몬|pokemon|포켓몬스터", "포켓몬스터", text)
        text = re.sub(r"젤다의전설|젤다|zelda", "젤다의 전설", text)
        text = re.sub(r"엘든링|elden ring", "엘든링", text)
        text = re.sub(r"csgo|카운터스트라이크|카스", "카운터스트라이크", text)
        text = re.sub(r"파이널판타지|ff", "파이널판타지", text)
        text = re.sub(r"디아블로|diablo|디아", "디아블로", text)
        text = re.sub(r"데드 바이 데이라이트|dbd|데바데", "데드 바이 데이라이트", text)
        text = re.sub(r"포트나이트|fortnite|포나", "포트나이트", text)
        text = re.sub(r"도타2|dota2", "도타2", text)
        text = re.sub(r"에이펙스 레전드|apex|에이팩스|에팩", "에이펙스 레전드", text)
        text = re.sub(r"메이플스토리|메이플|메플", "메이플스토리", text)
        text = re.sub(r"던전앤파이터|던파", "던전앤파이터", text)
        text = re.sub(r"블레이드앤소울|블소", "블레이드앤소울", text)
        text = re.sub(r"로스트아크|로아", "로스트아크", text)
        text = re.sub(r"서든어택|서든", "서든어택", text)
        text = re.sub(r"페이커|faker|대상혁|불사대마왕", "페이커", text)
        text = re.sub(r"gta|그타", "gta", text)
        text = re.sub(r"tft|롤토체스|롤체|전략적팀전투", "tft", text)
        text = re.sub(r"genshin impact|원신", "원신", text)
        text = re.sub(r"hearthstone|하스스톤|하스", "하스스톤", text)
        text = re.sub(r"clash of clans|클래시오브클랜|클오클", "클래시오브클랜", text)
        text = re.sub(r"brawl stars|브롤스타즈|브롤", "브롤스타즈", text)
        text = re.sub(r"among us|어몽어스|어몽", "어몽어스", text)
        text = re.sub(r"league of legends wild rift|와일드리프트|롤모바일", "와일드리프트", text)
        text = re.sub(r"animal crossing|동물의숲|모동숲", "동물의숲", text)
        text = re.sub(r"mario|마리오|슈퍼마리오", "슈퍼마리오", text)
        text = re.sub(r"smash bros|스매시브라더스|스매브라", "스매시브라더스", text)
        text = re.sub(r"monster hunter|몬스터헌터|몬헌", "몬스터헌터", text)
        text = re.sub(r"red dead redemption|레드데드리뎀션|레데리", "레드데드리뎀션", text)
        text = re.sub(r"assassin's creed|어쌔신크리드|어크", "어쌔신크리드", text)
        text = re.sub(r"resident evil|바이오하자드|레지던트이블", "바이오하자드", text)
        text = re.sub(r"the last of us|라스트오브어스|라오어", "라스트오브어스", text)
        text = re.sub(r"rainbow six siege|레인보우식스|레식", "레인보우식스", text)
        text = re.sub(r"street fighter|스트리트파이터|스트파", "스트리트파이터", text)
        text = re.sub(r"granblue fantasy|그랑블루판타지|그랑블루", "그랑블루판타지", text)
        text = re.sub(r"fps|퍼스트퍼슨슈터|1인칭슈팅", "FPS", text)
        text = re.sub(r"tps|3인칭슈팅|서드퍼슨슈터", "TPS", text)
        text = re.sub(r"metal gear solid|메탈기어솔리드|메기솔", "메탈기어솔리드", text)
        text = re.sub(r"support|서포터|서폿", "서포터", text)
        text = re.sub(r"ps5|플스5|플레이스테이션5", "플레이스테이션5", text)
        text = re.sub(r"xbox|엑스박스|엑박", "엑스박스", text)
        text = re.sub(r"nintendo|닌텐도|스위치", "닌텐도 스위치", text)
        text = re.sub(r"mobile|모바일|스마트폰게임", "모바일게임", text)
        text = re.sub(r"vr|가상현실|vr게임", "VR", text)
        text = re.sub(r"e-sports|이스포츠|e스포츠", "이스포츠", text)
        text = re.sub(r"skin|스킨|외형아이템", "스킨", text)
        text = re.sub(r"loot box|가챠|랜덤박스", "가챠", text)
        text = re.sub(r"season pass|배틀패스|시즌패스", "배틀패스", text)
        text = re.sub(r"chovy|쵸비|정지훈", "쵸비", text)
        text = re.sub(r"deft|데프트|김혁규", "데프트", text)
        text = re.sub(r"canyon|캐니언|김건부", "캐니언", text)
        text = re.sub(r"showmaker|쇼메이커|허수", "쇼메이커", text)
        text = re.sub(r"gumayusi|구마유시|이민형", "구마유시", text)
        text = re.sub(r"ruler|룰러|박재혁", "룰러", text)
        text = re.sub(r"zeus|제우스|최우제", "제우스", text)
        text = re.sub(r"keria|케리아|류민석", "케리아", text)
        text = re.sub(r"bengi|벵기|배성웅|뱅기", "벵기", text)
        text = re.sub(r"scout|스카웃|이예찬", "스카웃", text)
        text = re.sub(r"doran|도란|최현준", "도란", text)
        text = re.sub(r"bdd|비디디|곽보성", "비디디", text)
        text = re.sub(r"clid|클리드|김태민", "클리드", text)
        text = re.sub(r"peanut|피넛|한왕호", "피넛", text)
        text = re.sub(r"cuzz|커즈|문우찬", "커즈", text)
        # 게임 타이틀 및 장르
        text = re.sub(r"league\s*of\s*legends|lol", "리그 오브 레전드", text)
        text = re.sub(r"overwatch", "오버워치", text)
        text = re.sub(r"dota\s*2", "도타 2", text)
        text = re.sub(r"counter\s*strike[:]?[\s]*global\s*offensive|cs:go|csgo", "카운터 스트라이크: 글로벌 오펜시브", text)
        text = re.sub(r"call\s*of\s*duty", "콜 오브 듀티", text)
        text = re.sub(r"battlefield", "배틀필드", text)
        text = re.sub(r"valorant", "발로란트", text)
        text = re.sub(r"fortnite", "포트나이트", text)
        text = re.sub(r"apex\s*legends", "에이펙스 레전드", text)
        text = re.sub(r"pubg|playerunknown'?s\s*battlegrounds", "플레이어언노운스 배틀그라운드", text)
        text = re.sub(r"freefire", "프리파이어", text)
        text = re.sub(r"rocket\s*league", "로켓 리그", text)
        text = re.sub(r"minecraft", "마인크래프트", text)
        text = re.sub(r"roblox", "로블록스", text)
        text = re.sub(r"among\s*us", "어몽 어스", text)
        text = re.sub(r"fall\s*guys", "폴 가이즈", text)
        text = re.sub(r"world\s*of\s*warcraft", "월드 오브 워크래프트", text)
        text = re.sub(r"diablo\s*\d*", "디아블로", text)
        text = re.sub(r"starcraft\s*ii", "스타크래프트 2", text)
        text = re.sub(r"starcraft", "스타크래프트", text)
        text = re.sub(r"warcraft", "워크래프트", text)
        text = re.sub(r"smite", "스마이트", text)
        text = re.sub(r"paladins", "팔라딘", text)
        text = re.sub(r"rainbow\s*six\s*siege", "레인보우 식스 시즈", text)
        text = re.sub(r"fifa", "피파", text)
        text = re.sub(r"nba2k", "엔비에이투케이", text)
        text = re.sub(r"madden", "매든", text)
        text = re.sub(r"pes", "피에스", text)
        text = re.sub(r"need\s*for\s*speed", "니드 포 스피드", text)
        text = re.sub(r"gran\s*turismo", "그란 투리스모", text)
        text = re.sub(r"forza\s*horizon", "포르자 호라이즌", text)
        text = re.sub(r"the\s*sims", "더 심즈", text)
        text = re.sub(r"simcity", "심시티", text)
        text = re.sub(r"civilization", "문명", text)
        text = re.sub(r"age\s*of\s*empires", "에이지 오브 엠파이어", text)
        text = re.sub(r"strategy", "전략", text)
        text = re.sub(r"simulation", "시뮬레이션", text)
        text = re.sub(r"sandbox", "샌드박스", text)
        text = re.sub(r"survival", "서바이벌", text)
        text = re.sub(r"adventure", "어드벤처", text)
        text = re.sub(r"fighting", "격투", text)
        text = re.sub(r"sports", "스포츠", text)
        
        # e스포츠 팀 및 대회
        text = re.sub(r"skt\s*t1", "skt t1", text, flags=re.IGNORECASE)
        text = re.sub(r"gen\.?\s*g", "gen.g", text, flags=re.IGNORECASE)
        text = re.sub(r"damwon", "담원", text, flags=re.IGNORECASE)
        text = re.sub(r"fnatic", "프나틱", text, flags=re.IGNORECASE)
        text = re.sub(r"team\s*liquid", "팀 리퀴드", text, flags=re.IGNORECASE)
        text = re.sub(r"cloud9", "클라우드 나인", text, flags=re.IGNORECASE)
        text = re.sub(r"g2\s*esports", "g2 esports", text, flags=re.IGNORECASE)
        text = re.sub(r"team\s*solomid", "팀 솔로미드", text, flags=re.IGNORECASE)
        text = re.sub(r"evil\s*geniuses", "이빌 지니어스", text, flags=re.IGNORECASE)
        text = re.sub(r"\bog\b", "오지", text, flags=re.IGNORECASE)
        text = re.sub(r"virtus\.?pro", "비르투스 프로", text, flags=re.IGNORECASE)
        text = re.sub(r"natus\s*vincere", "나투스 빈체레", text, flags=re.IGNORECASE)
        text = re.sub(r"astralis", "아스트랄리스", text, flags=re.IGNORECASE)
        text = re.sub(r"ence", "엔스", text, flags=re.IGNORECASE)
        text = re.sub(r"ninjas\s*in\s*pyjamas", "닌자스 인 파자마스", text, flags=re.IGNORECASE)
        text = re.sub(r"faze\s*clan", "페이즈 클랜", text, flags=re.IGNORECASE)
        text = re.sub(r"100\s*thieves", "100 시브스", text, flags=re.IGNORECASE)
        text = re.sub(r"mineski", "마인스키", text, flags=re.IGNORECASE)
        text = re.sub(r"royal\s*never\s*give\s*up", "로열 네버 기브 업", text, flags=re.IGNORECASE)
        text = re.sub(r"invictus\s*gaming", "인빅터스 게이밍", text, flags=re.IGNORECASE)
        text = re.sub(r"edward\s*gaming", "에드워드 게이밍", text, flags=re.IGNORECASE)
        text = re.sub(r"top\s*esports", "탑 이스포츠", text, flags=re.IGNORECASE)
        text = re.sub(r"rare\s*atom", "레어 애텀", text, flags=re.IGNORECASE)
        text = re.sub(r"drx", "drx", text, flags=re.IGNORECASE)
        
        # 게임 플랫폼 및 스토어
        text = re.sub(r"pc", "pc", text, flags=re.IGNORECASE)
        text = re.sub(r"xbox\s*series\s*x", "xbox series x", text, flags=re.IGNORECASE)
        text = re.sub(r"playstation\s*5", "플레이스테이션 5", text, flags=re.IGNORECASE)
        text = re.sub(r"steam", "스팀", text, flags=re.IGNORECASE)
        text = re.sub(r"epic\s*games\s*store", "에픽 게임즈 스토어", text, flags=re.IGNORECASE)
        text = re.sub(r"origin", "오리진", text, flags=re.IGNORECASE)
        text = re.sub(r"battle\.?net", "배틀넷", text, flags=re.IGNORECASE)
        text = re.sub(r"uplay", "유플레이", text, flags=re.IGNORECASE)
        text = re.sub(r"gog", "gog", text, flags=re.IGNORECASE)
        text = re.sub(r"itch\.?io", "itch.io", text, flags=re.IGNORECASE)
        
        # 하드웨어 및 주변기기
        text = re.sub(r"gaming\s*mouse", "게이밍 마우스", text, flags=re.IGNORECASE)
        text = re.sub(r"gaming\s*keyboard", "게이밍 키보드", text, flags=re.IGNORECASE)
        text = re.sub(r"mechanical\s*keyboard", "기계식 키보드", text, flags=re.IGNORECASE)
        text = re.sub(r"gaming\s*headset", "게이밍 헤드셋", text, flags=re.IGNORECASE)
        text = re.sub(r"gaming\s*monitor", "게이밍 모니터", text, flags=re.IGNORECASE)
        text = re.sub(r"gaming\s*chair", "게이밍 체어", text, flags=re.IGNORECASE)
        text = re.sub(r"rgb", "rgb", text, flags=re.IGNORECASE)
        text = re.sub(r"gaming\s*pc", "게이밍 pc", text, flags=re.IGNORECASE)
        text = re.sub(r"laptop", "노트북", text, flags=re.IGNORECASE)
        
        # 게이밍 콘텐츠 크리에이터
        text = re.sub(r"ninja", "닌자", text, flags=re.IGNORECASE)
        text = re.sub(r"shroud", "슈라우드", text, flags=re.IGNORECASE)
        text = re.sub(r"pokimane", "포키메인", text, flags=re.IGNORECASE)
        text = re.sub(r"tfue", "티퓨", text, flags=re.IGNORECASE)
        text = re.sub(r"summit1g", "서밋1g", text, flags=re.IGNORECASE)
        text = re.sub(r"drdisrespect", "드디스", text, flags=re.IGNORECASE)
        text = re.sub(r"timthetatman", "팀더탯맨", text, flags=re.IGNORECASE)
        text = re.sub(r"couragejd", "커레이지JD", text, flags=re.IGNORECASE)
        text = re.sub(r"sypherpk", "사이퍼PK", text, flags=re.IGNORECASE)
        text = re.sub(r"myth", "마이스", text, flags=re.IGNORECASE)
        text = re.sub(r"dakotaz", "다코타즈", text, flags=re.IGNORECASE)
        text = re.sub(r"lirik", "리릭", text, flags=re.IGNORECASE)
        text = re.sub(r"xqc", "엑스큐시", text, flags=re.IGNORECASE)
        text = re.sub(r"sodapoppin", "소다팝핀", text, flags=re.IGNORECASE)
        text = re.sub(r"tommmy", "토미", text, flags=re.IGNORECASE)
        text = re.sub(r"tranq", "트랭크", text, flags=re.IGNORECASE)
        
        # 게임 장르 및 기타 용어
        text = re.sub(r"fps", "fps", text, flags=re.IGNORECASE)
        text = re.sub(r"rpg", "rpg", text, flags=re.IGNORECASE)
        text = re.sub(r"moba", "moba", text, flags=re.IGNORECASE)
        text = re.sub(r"battle\s*royale", "배틀로얄", text, flags=re.IGNORECASE)
        text = re.sub(r"rts", "rts", text, flags=re.IGNORECASE)
        text = re.sub(r"esports", "이스포츠", text, flags=re.IGNORECASE)
        text = re.sub(r"competitive\s*gaming", "경쟁 게임", text, flags=re.IGNORECASE)
        text = re.sub(r"casual\s*gaming", "캐주얼 게임", text, flags=re.IGNORECASE)
        text = re.sub(r"multiplayer", "멀티플레이어", text, flags=re.IGNORECASE)
        text = re.sub(r"singleplayer", "싱글플레이어", text, flags=re.IGNORECASE)
        text = re.sub(r"co[-\s]?op", "협동", text, flags=re.IGNORECASE)
        text = re.sub(r"free[-\s]?to[-\s]?play", "무료플레이", text, flags=re.IGNORECASE)
        text = re.sub(r"pay[-\s]?to[-\s]?win", "페이투윈", text, flags=re.IGNORECASE)
        text = re.sub(r"dlc", "dlc", text, flags=re.IGNORECASE)
        text = re.sub(r"patch", "패치", text, flags=re.IGNORECASE)
        text = re.sub(r"update", "업데이트", text, flags=re.IGNORECASE)
        text = re.sub(r"beta", "베타", text, flags=re.IGNORECASE)
        text = re.sub(r"alpha", "알파", text, flags=re.IGNORECASE)
        text = re.sub(r"early\s*access", "얼리 액세스", text, flags=re.IGNORECASE)
        text = re.sub(r"patch\s*note", "패치 노트", text, flags=re.IGNORECASE)
        text = re.sub(r"season\s*pass", "시즌 패스", text, flags=re.IGNORECASE)
        text = re.sub(r"live\s*service", "라이브 서비스", text, flags=re.IGNORECASE)
        text = re.sub(r"microtransactions", "마이크로트랜잭션", text, flags=re.IGNORECASE)
    elif category == "Science & Technology":
    # IT 및 대형 기술 기업
        text = re.sub(r"google", "구글", text, flags=re.IGNORECASE)
        text = re.sub(r"apple", "애플", text, flags=re.IGNORECASE)
        text = re.sub(r"microsoft", "마이크로소프트", text, flags=re.IGNORECASE)
        text = re.sub(r"amazon", "아마존", text, flags=re.IGNORECASE)
        text = re.sub(r"facebook", "페이스북", text, flags=re.IGNORECASE)
        text = re.sub(r"twitter", "트위터", text, flags=re.IGNORECASE)
        text = re.sub(r"linkedin", "링크드인", text, flags=re.IGNORECASE)
        text = re.sub(r"samsung", "삼성", text, flags=re.IGNORECASE)
        text = re.sub(r"lg", "엘지", text, flags=re.IGNORECASE)
        text = re.sub(r"sony", "소니", text, flags=re.IGNORECASE)
        text = re.sub(r"intel", "인텔", text, flags=re.IGNORECASE)
        text = re.sub(r"ibm", "아이비엠", text, flags=re.IGNORECASE)
        text = re.sub(r"tesla", "테슬라", text, flags=re.IGNORECASE)
        text = re.sub(r"spacex", "스페이스엑스", text, flags=re.IGNORECASE)
        text = re.sub(r"nasa", "나사", text, flags=re.IGNORECASE)
        
        # 학술 및 연구 기관
        text = re.sub(r"mit", "MIT", text, flags=re.IGNORECASE)
        text = re.sub(r"stanford", "스탠포드", text, flags=re.IGNORECASE)
        text = re.sub(r"harvard", "하버드", text, flags=re.IGNORECASE)
        text = re.sub(r"oxford", "옥스포드", text, flags=re.IGNORECASE)
        text = re.sub(r"cambridge", "케임브리지", text, flags=re.IGNORECASE)
        text = re.sub(r"caltech", "캘리포니아 공과대학교", text, flags=re.IGNORECASE)
        
        # 기타 IT/테크 기업
        text = re.sub(r"oracle", "오라클", text, flags=re.IGNORECASE)
        text = re.sub(r"sap", "SAP", text, flags=re.IGNORECASE)
        text = re.sub(r"salesforce", "세일즈포스", text, flags=re.IGNORECASE)
        text = re.sub(r"ebay", "이베이", text, flags=re.IGNORECASE)
        text = re.sub(r"alibaba", "알리바바", text, flags=re.IGNORECASE)
        text = re.sub(r"tencent", "텐센트", text, flags=re.IGNORECASE)
        text = re.sub(r"baidu", "바이두", text, flags=re.IGNORECASE)
        text = re.sub(r"jd\.?com", "JD.com", text, flags=re.IGNORECASE)
        text = re.sub(r"pinduoduo", "핀두오두오", text, flags=re.IGNORECASE)
        text = re.sub(r"softbank", "소프트뱅크", text, flags=re.IGNORECASE)
        text = re.sub(r"broadcom", "브로드컴", text, flags=re.IGNORECASE)
        text = re.sub(r"texas\s*instruments", "텍사스 인스트루먼트", text, flags=re.IGNORECASE)
        text = re.sub(r"micron", "마이크론", text, flags=re.IGNORECASE)
        text = re.sub(r"seagate", "시게이트", text, flags=re.IGNORECASE)
        text = re.sub(r"western\s*digital", "웨스턴 디지털", text, flags=re.IGNORECASE)
        
        # 소프트웨어, 프로그래밍 언어 및 개발 도구
        text = re.sub(r"python", "파이썬", text, flags=re.IGNORECASE)
        text = re.sub(r"java", "자바", text, flags=re.IGNORECASE)
        text = re.sub(r"c\+\+", "씨 플러스 플러스", text, flags=re.IGNORECASE)
        text = re.sub(r"javascript", "자바스크립트", text, flags=re.IGNORECASE)
        text = re.sub(r"html", "HTML", text, flags=re.IGNORECASE)
        text = re.sub(r"css", "CSS", text, flags=re.IGNORECASE)
        text = re.sub(r"ruby", "루비", text, flags=re.IGNORECASE)
        text = re.sub(r"php", "피에이치피", text, flags=re.IGNORECASE)
        text = re.sub(r"go(lang)?", "고", text, flags=re.IGNORECASE)
        text = re.sub(r"swift", "스위프트", text, flags=re.IGNORECASE)
        text = re.sub(r"kotlin", "코틀린", text, flags=re.IGNORECASE)
        text = re.sub(r"r\s*programming", "알 프로그래밍", text, flags=re.IGNORECASE)
        text = re.sub(r"sql", "SQL", text, flags=re.IGNORECASE)
        text = re.sub(r"nosql", "NoSQL", text, flags=re.IGNORECASE)
        text = re.sub(r"tensorflow", "텐서플로", text, flags=re.IGNORECASE)
        text = re.sub(r"pytorch", "파이토치", text, flags=re.IGNORECASE)
        text = re.sub(r"keras", "케라스", text, flags=re.IGNORECASE)
        text = re.sub(r"scikit[-\s]?learn", "사이킷런", text, flags=re.IGNORECASE)
        text = re.sub(r"opencv", "오픈씨브이", text, flags=re.IGNORECASE)
        text = re.sub(r"docker", "도커", text, flags=re.IGNORECASE)
        text = re.sub(r"kubernetes", "쿠버네티스", text, flags=re.IGNORECASE)
        text = re.sub(r"aws", "아마존 웹 서비스", text, flags=re.IGNORECASE)
        text = re.sub(r"azure", "애저", text, flags=re.IGNORECASE)
        text = re.sub(r"gcp", "구글 클라우드", text, flags=re.IGNORECASE)
        text = re.sub(r"big\s*data", "빅데이터", text, flags=re.IGNORECASE)
        text = re.sub(r"blockchain", "블록체인", text, flags=re.IGNORECASE)
        text = re.sub(r"cryptocurrency", "암호화폐", text, flags=re.IGNORECASE)
        text = re.sub(r"bitcoin", "비트코인", text, flags=re.IGNORECASE)
        text = re.sub(r"ethereum", "이더리움", text, flags=re.IGNORECASE)
        text = re.sub(r"ai", "인공지능", text, flags=re.IGNORECASE)
        text = re.sub(r"machine\s*learning", "머신러닝", text, flags=re.IGNORECASE)
        text = re.sub(r"deep\s*learning", "딥러닝", text, flags=re.IGNORECASE)
        text = re.sub(r"neural\s*network", "신경망", text, flags=re.IGNORECASE)
        text = re.sub(r"iot", "사물인터넷", text, flags=re.IGNORECASE)
        
        # 하드웨어, 전자제품 및 반도체 관련
        text = re.sub(r"semiconductor", "반도체", text, flags=re.IGNORECASE)
        text = re.sub(r"microchip", "마이크로칩", text, flags=re.IGNORECASE)
        text = re.sub(r"lcd", "LCD", text, flags=re.IGNORECASE)
        text = re.sub(r"led", "LED", text, flags=re.IGNORECASE)
        text = re.sub(r"oled", "OLED", text, flags=re.IGNORECASE)
        text = re.sub(r"vlsi", "VLSI", text, flags=re.IGNORECASE)
        text = re.sub(r"fpga", "FPGA", text, flags=re.IGNORECASE)
        text = re.sub(r"bios", "BIOS", text, flags=re.IGNORECASE)
        text = re.sub(r"motherboard", "메인보드", text, flags=re.IGNORECASE)
        text = re.sub(r"cpu", "CPU", text, flags=re.IGNORECASE)
        text = re.sub(r"gpu", "GPU", text, flags=re.IGNORECASE)
        text = re.sub(r"ram", "램", text, flags=re.IGNORECASE)
        text = re.sub(r"ssd", "SSD", text, flags=re.IGNORECASE)
        text = re.sub(r"hdd", "HDD", text, flags=re.IGNORECASE)
        text = re.sub(r"storage", "스토리지", text, flags=re.IGNORECASE)
        text = re.sub(r"router", "라우터", text, flags=re.IGNORECASE)
        text = re.sub(r"modem", "모뎀", text, flags=re.IGNORECASE)
        
        # 기타 기술 용어 및 신기술
        text = re.sub(r"quantum\s*computing", "양자 컴퓨팅", text, flags=re.IGNORECASE)
        text = re.sub(r"nanotechnology", "나노기술", text, flags=re.IGNORECASE)
        text = re.sub(r"biotechnology", "바이오테크놀로지", text, flags=re.IGNORECASE)
        text = re.sub(r"genomics", "유전체학", text, flags=re.IGNORECASE)
        text = re.sub(r"robotics", "로보틱스", text, flags=re.IGNORECASE)
        text = re.sub(r"automation", "자동화", text, flags=re.IGNORECASE)
        text = re.sub(r"satellite", "위성", text, flags=re.IGNORECASE)
        text = re.sub(r"space\s*exploration", "우주 탐사", text, flags=re.IGNORECASE)

    # 중복 공백 제거
    text = re.sub(r'\s{2,}', ' ', text)
    # 앞뒤 공백 제거
    text = text.strip()
     # 영어 제거
    text = re.sub(r'[a-zA-Z]', ' ', text)
    
    # 중복 공백 제거
    text = re.sub(r'\s{2,}', ' ', text)
    
    text = re.sub(r"[^가-힣a-zA-Z0-9\s]", "", text)
    

    return text


# YOUTUBE API를 통해 동영상 데이터 가져오기
def fetch_trending_videos(category_id, max_results=200):
    
    region_code="KR"
    videos = []
    next_page_token = None

    while len(videos) < max_results:
        try:
            request = youtube.videos().list(
                part="snippet,statistics,contentDetails",
                chart="mostPopular",
                regionCode=region_code,
                videoCategoryId=category_id,
                maxResults=min(50, max_results - len(videos)),
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get("items", []):
                duration = isodate.parse_duration(item["contentDetails"]["duration"])
                duration_in_seconds = duration.total_seconds()  #초로 바꾸기기

                if duration_in_seconds > 90:  # 80초 이상의 동영상만 가져오기
                    videos.append({
                        "video_id": item["id"],
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "tags": item["snippet"].get("tags", []),
                        "duration": str(duration),
                        "view_count": int(item["statistics"].get("viewCount", 0)),
                        "like_count": int(item["statistics"].get("likeCount", 0)),
                        "comment_count": int(item["statistics"].get("commentCount", 0)),
                        "category_id": category_id,
                    })

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        except Exception as e:
            print(f"Error fetching videos: {e}")
            time.sleep(5)  # 잠시 대기 후 다시 시도

    return videos

# 댓글 가져오기기
def fetch_video_comments(video_id, max_results=100):
    comments = []
    next_page_token = None

    while len(comments) < max_results:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(50, max_results - len(comments)),
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                if not comments:
                    print(f"{video_id} - 댓글 없음")
                break

        except Exception as e:
            break

    return comments

# mongoDB에 데이터 저장하기
def store_trending_videos_with_comments():
    db =mg_client["howabout"]
    
    formatted_videos = []  # 새로운 데이터만 저장할 리스트
    updated_count = 0  # 업데이트된 동영상 개수

    for category_name, category_id in CATEGORIES.items():
        print(f"'{category_name}'동영상 가져오는 중...")

        # 1️⃣ 인기 동영상 가져오기
        videos = fetch_trending_videos(category_id, max_results=200)

        for video in videos:
            video_id = video["video_id"]

            # 2️⃣ 해당 동영상의 댓글 가져오기
            comments = fetch_video_comments(video_id, max_results=100)
            cleaned_comments = [clean_text(comment, category_name) for comment in comments]
            
            video_data = {
                "timestamp": datetime.now(),  # 현재 시간 (UTC)
                "metadata": {"category_id": category_id},
                "video_id": video["video_id"],
                "title": video["title"],
                "description": video["description"],
                "tags": video["tags"],
                "duration": video["duration"],
                "view_count": video["view_count"],
                "like_count": video["like_count"],
                "comment_count": video["comment_count"],
                "comments": cleaned_comments  # 댓글 추가
            }

            # 3️⃣ 기존 데이터 확인 후 삭제 후 삽입 (update 대신 delete + insert)
            existing_video = db.video_trends.find_one({"video_id": video_id})
            if existing_video:
                db.video_trends.delete_one({"video_id": video_id})  # 기존 데이터 삭제
                print(f"기존 데이터 삭제: {video_id}")
                updated_count += 1
            
            formatted_videos.append(video_data)  # 새 데이터 추가

    # 4️⃣ 새로운 데이터만 MongoDB에 저장
    if formatted_videos:
        db.raw_video_data.insert_many(formatted_videos)
        print(f"✅ {len(formatted_videos)}개의 새로운 동영상 + 댓글 데이터 저장 완료.")
    else:
        print("✅ 새로운 데이터가 없어 추가 저장하지 않음.")

    print(f"🔄 총 {updated_count}개의 동영상이 업데이트됨.")

    # 5️⃣ 저장된 데이터 개수 출력
    for category_name, category_id in CATEGORIES.items():
        video_count = db.raw_video_data.count_documents({"metadata.category_id": category_id})
        comment_count = sum([len(video["comments"]) for video in db.raw_video_data.find({"metadata.category_id": category_id})])
        print(f"📊 카테고리: {category_name} - 동영상 수: {video_count}, 댓글 수: {comment_count}")