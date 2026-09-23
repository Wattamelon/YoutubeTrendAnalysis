import yt_dlp
import os
from openai import OpenAI
import tiktoken
from dotenv import load_dotenv


# OpenAI 클라이언트 초기화 (API 키는 환경변수에서 읽기)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def download_audio_if_short(url, save_dir="audios"):
    os.makedirs(save_dir, exist_ok=True)

    # 메타데이터 먼저 추출 (길이 확인용)
    ydl_opts_metadata = {
        'quiet': True,
        'skip_download': True,
        'format': 'bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts_metadata) as ydl:
        info = ydl.extract_info(url, download=False)
        duration = info.get("duration", 0)  # 단위: 초
        title = info.get("title", "untitled")
        video_id = info.get("id")

    if duration > 900:  # 15분 초과
        print("⛔ 15분 이상 동영상은 지원하지 않습니다.")
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
    }

    with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
        ydl.download([url])

    mp3_path = os.path.join(save_dir, f"{video_id}.mp3")
    print(f"✅ 오디오 다운로드 완료: {mp3_path}")
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
        raise FileNotFoundError(f"❌ 파일을 찾을 수 없습니다: {audio_path}")
    
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
            language=language
        )

    return response


# 💰 요금 기준 (2025년 GPT-4 Turbo 기준)
COST_PER_1K_INPUT = 0.01
COST_PER_1K_OUTPUT = 0.03

def count_tokens(text, model="gpt-4-turbo"):
    """입력 텍스트의 토큰 수 계산"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def summarize_youtube_text(text: str, model: str = "gpt-4-turbo") -> dict:
    """
    GPT-4 Turbo로 유튜브 전체 텍스트를 요약하고 키워드를 추출합니다.

    Parameters:
        text (str): Whisper 등으로 얻은 전체 자막 텍스트
        model (str): 사용할 OpenAI 모델 이름

    Returns:
        dict: 요약 결과, 키워드 리스트, 토큰 수, 예상 비용 등 포함
    """

    prompt = f"""
다음은 유튜브 방송의 전체 텍스트야.
오타가 조금 많으니 너가 알아서 고쳐주고,
전체적인 내용을 3줄로 요약해주고,
중요한 키워드 5개를 뽑아줘.
가장 중요한 키워드부터 순서대로 나열해줘.

{text}
    """.strip()

    input_tokens = count_tokens(prompt, model)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content
    output_tokens = count_tokens(reply, model)

    estimated_cost = (input_tokens / 1000) * COST_PER_1K_INPUT + (output_tokens / 1000) * COST_PER_1K_OUTPUT

    return {
        "summary_text": reply,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost": round(estimated_cost, 5)
    }
    
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("audio.py : 유튜브 링크가 필요합니다.")
        sys.exit(1)

    url = sys.argv[1]

    # 1. 오디오 다운로드
    audio_path = download_audio_if_short(url)
    if not audio_path:
        print("audio.py : 오디오 다운로드 실패 또는 15분 초과")
        sys.exit(1)

    # 2. Whisper 전사
    transcript = transcribe_with_whisper_api(audio_path)

    # 3. GPT 요약
    result = summarize_youtube_text(transcript)

    # 4. 요약 결과 출력 (JSON으로 반환)
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
