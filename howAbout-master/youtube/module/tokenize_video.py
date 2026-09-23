from kiwipiepy.utils import Stopwords
from init import english_stopwords

def tokenize_video(data, kiwi_objects): 
    stopwords = Stopwords()
    stopwords.add(english_stopwords)
    stopwords.add("사랑해요")
    stopwords.add("안녕하세요")
    stopwords.add("사랑합니다")
    stopwords.add("한국")


    proccessed_data = {}
    
    for category, videos in data.items():
        proccessed_data[category] = []
        for video in videos:
            # 댓글
            comments = video.get("comments", [])
            comments_text = "\n".join(comments)
            
            # 제목
            title_text = video.get("title", "")
            tags = video.get("tags", [])
            
            title_tokens = kiwi_objects[category].tokenize(title_text, stopwords=stopwords)
            comments_tokens = kiwi_objects[category].tokenize(comments_text, stopwords=stopwords)
            
            title_nouns = [
            token.form for token in title_tokens
            if token.tag in ["NNP", "SL"] and len(token.form) > 1
            ]
            tags_nouns = list(set(tags))  # 중복 제거
            tags_nouns = [tag for tag in tags_nouns if tag.strip() and len(tag.strip()) > 1]
            comments_nouns = [
            token.form for token in comments_tokens
            if token.tag in ["NNP", "SL"] and len(token.form) > 1
            ]
            
            video["title_nouns"] = title_nouns
            video["tag_nouns"] = tags_nouns
            video["comments_nouns"] = comments_nouns
            video["comments"] = []
            proccessed_data[category].append(video)
            
    return proccessed_data
            
def tokenize_related_video(data, kiwi_objects): 

    stopwords = Stopwords()
    stopwords.add(english_stopwords)
    stopwords.add("사랑해요")
    stopwords.add("안녕하세요")
    stopwords.add("한국")

    proccessed_data = {}
    for category, videos in data.items():
        proccessed_data[category] = []
        for video in videos:
            # 제목
            title_text = video.get("title", "")
            tags = video.get("tags", [])
            
            title_tokens = kiwi_objects[category].tokenize(title_text, stopwords=stopwords)
            comments_noun_list = []
            # 댓글
            for comment in video.get("comments", []):
                comments_tokens = kiwi_objects[category].tokenize(comment, stopwords=stopwords)
                comments_nouns = [
                token.form for token in comments_tokens
                if token.tag in ["NNP","NNG", "SL"] and len(token.form) > 1
                ]
                comments_noun_list.append(comments_nouns)
            
            
            title_nouns = [
            token.form for token in title_tokens
            if token.tag in ["NNP", "SL"] and len(token.form) > 1
            ]
            tags_nouns = list(set(tags))  # 중복 제거
            tags_nouns = [tag for tag in tags_nouns if tag.strip() and len(tag.strip()) > 1]
            
            
            video["title_nouns"] = title_nouns
            video["tag_nouns"] = tags_nouns
            video["comments_noun_list"] = comments_noun_list
            video["comments"] = []
            proccessed_data[category].append(video)
    
    
    return proccessed_data