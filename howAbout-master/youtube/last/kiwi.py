from kiwipiepy import Kiwi

def make_kiwi(data):
    kiwi_objects = {}
    
    for category, videos in data.items():
        kiwi = Kiwi()
        new_word_cnt = kiwi.load_user_dictionary("user_dict.txt")
        print(new_word_cnt)
        
        category_comments = []
        for video in videos:
            comments = video.get("comments", [])
            #띄어쓰기
            spaced_comments = []
            for comment in comments:
                spaced_comment = kiwi.space(comment, reset_whitespace = True)
                spaced_comments.append(spaced_comment)
            video_comment = " ".join(spaced_comments)
            
            video_comment = " ".join(comments)
            category_comments.append(video_comment)
        # 학습된 단어 확인
        print(f"Category: {category}")
        scores = kiwi.extract_add_words(category_comments, min_cnt=5, max_word_len=10, min_score=0.1, pos_score= 0.0)
        for word, final_score, freq, pos_score in scores:
            print(f"단어: {word}, 점수: {final_score:.3f}, 출현 빈도: {freq}, 품사 점수: {pos_score:.3f}")

        kiwi_objects[category] = kiwi 
    
    return kiwi_objects