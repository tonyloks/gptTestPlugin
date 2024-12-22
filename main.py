from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

# Если будете использовать GPT-сжатие
# import openai
# openai.api_key = "ВАШ_API_КЛЮЧ"

app = FastAPI(
    title="YouTube Summary Plugin",
    description="Плагин для получения краткого содержания YouTube-видео",
    version="0.0.1"
)

class SummaryRequest(BaseModel):
    youtube_url: str

class SummaryResponse(BaseModel):
    summary: str

@app.post("/summary", response_model=SummaryResponse)
def get_summary(request: SummaryRequest):
    """
    Возвращает краткое содержание ролика по ссылке на YouTube.
    """
    youtube_url = request.youtube_url

    # 1. Получаем идентификатор видео из youtube_url
    #    Простейший вариант (можно улучшать парсинг):
    import re
    match = re.search(r"v=([^&]+)", youtube_url)
    if not match:
        return {"summary": "Не удалось найти ID видео в ссылке"}

    video_id = match.group(1)

    # 2. Получаем транскрипт (если доступен)
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ru', 'en'])
    except Exception as e:
        return {"summary": f"Ошибка при получении транскрипта: {str(e)}"}

    # 3. Объединяем текст
    full_text = " ".join([item['text'] for item in transcript])

    # 4. Сжимаем текст
    # Вариант A: Использовать OpenAI GPT для сжатия (при наличии api_key)
    # short_text = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=f"Сжать текст до 3-5 предложений:\n\n{full_text}",
    #     max_tokens=200
    # )
    # summary = short_text.choices[0].text.strip()

    # Вариант B: Простейшая "заглушка"-сокращалка (место для ваших алгоритмов):
    words = full_text.split()
    summary = " ".join(words[:100]) + "..." if len(words) > 100 else full_text

    return {"summary": summary}
