import yt_dlp
import os
from openai import OpenAI
import tiktoken
from dotenv import load_dotenv
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

class MyLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): print(msg, file=sys.stderr)

# OpenAI 클라이언트 초기화 (API 키는 환경변수에서 읽기)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def download_audio_if_short(url, save_dir="audios"):
    os.makedirs(save_dir, exist_ok=True)

    # 메타데이터 먼저 추출 (길이 확인용)
    ydl_opts_metadata = {
    'quiet': True,            # 👈 일반 로그 제거
    'skip_download': True,
    'format': 'bestaudio/best',
    'no_warnings': True,      # 👈 경고 제거
    'logger': MyLogger(),     # 👈 stdout 로그 제거용 커스텀 logger 설정
}

    with yt_dlp.YoutubeDL(ydl_opts_metadata) as ydl:
        info = ydl.extract_info(url, download=False)
        duration = info.get("duration", 0)  # 단위: 초
        title = info.get("title", "untitled")
        video_id = info.get("id")

    if duration > 900:  # 15분 초과
        print(" 15분 이상 동영상은 지원하지 않습니다.", file=sys.stderr)
        return None

    # 오디오 다운로드 설정
    output_path = os.path.join(save_dir, f"{video_id}.%(ext)s")

    ydl_opts_download = {
    'format': 'bestaudio/best',
    'outtmpl': output_path,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
    'no_warnings': True,
    'logger': MyLogger(),     # 👈 여기도 logger 설정
}

    with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
        ydl.download([url])

    mp3_path = os.path.join(save_dir, f"{video_id}.mp3")
    return mp3_path



def transcribe_with_whisper_api(audio_path: str, language: str = "ko") -> str:
    """
    OpenAI Whisper-1 API를 사용하여 오디오를 텍스트로 변환합니다.

    Parameters:
        audio_path (str): 변환할 오디오 파일의 경로 (mp3, wav 등)
        language (str): 언어 코드 (예: 'ko' - 한국어, 'en' - 영어 등)

    Returns:
        str: 변환된 텍스트 (자막)
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f" 파일을 찾을 수 없습니다: {audio_path}")
    
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
            language=language
        )

    return response

def summarize_youtube_text(text: str, model: str = "gpt-4.1") -> dict:
    """
    GPT-4 Turbo로 유튜브 전체 텍스트를 요약하고 키워드를 추출합니다.

    Parameters:
        text (str): Whisper 등으로 얻은 전체 자막 텍스트
        model (str): 사용할 OpenAI 모델 이름

    Returns:
        dict: 요약 결과, 키워드 리스트, 토큰 수, 예상 비용 등 포함
    """

    prompt = f"""
    너는 요약의 천재야.
    아래의 긴 텍스트를 요약해줘.
    전체 내용을 3문장으로 요약약해줘.
    3문장은 너무 길지 않게 해줘. 앞에 숫자를 붙여줘
    그리고 핵심 키워드 5개를 뽑아줘.
    세줄 요약 앞에 번호를 붙여줘.
    그리고 키워드 앞에도 번호를 붙여줘.

{text}
    """.strip()


    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content


    return {
        "summary_text": reply,
        
    }
    
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("audio.py : 유튜브 링크가 필요합니다.", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]

    # 1. 오디오 다운로드
    audio_path = download_audio_if_short(url)
    if not audio_path:
        print("audio.py : 오디오 다운로드 실패 또는 15분 초과", file=sys.stderr)
        sys.exit(1)

    # 2. Whisper 전사
    transcript = transcribe_with_whisper_api(audio_path)

    # 3. GPT 요약
    result = summarize_youtube_text(transcript)

    # 4. 요약 결과 출력 (JSON으로 반환)
    import json
    print(json.dumps(result, ensure_ascii=False))
    