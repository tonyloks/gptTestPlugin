from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="YouTube Summary Plugin",
    description="Плагин для получения краткого содержания YouTube-видео",
    version="0.0.1"
)

# Отладка: посмотрим, какая у нас рабочая директория при запуске
print("Текущая рабочая директория (os.getcwd()):", os.getcwd())
print("Папка, где лежит этот скрипт (__file__):", __file__)
print("os.path.dirname(__file__):", os.path.dirname(__file__))

# Путь к папке .well-known
directory_path = os.path.join(os.path.dirname(__file__), ".well-known")

print("directory_path =", directory_path)

# Создаём папку, если её нет
if not os.path.exists(directory_path):
    try:
        os.makedirs(directory_path)
        print(f"Папка '{directory_path}' успешно создана.")
    except Exception as e:
        print(f"Ошибка при создании папки: {e}")
else:
    print(f"Папка '{directory_path}' уже существует.")

# Проверяем права на чтение
print("Папка доступна для чтения?", os.access(directory_path, os.R_OK))

# Проверяем, что в папке действительно лежит ai-plugin.json
file_path = os.path.join(directory_path, "ai-plugin.json")
print("Путь к файлу ai-plugin.json:", file_path)
print("Существует ли файл?", os.path.exists(file_path))

if os.path.exists(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print("Содержимое ai-plugin.json:")
        print(content)
    except Exception as e:
        print("Ошибка при чтении ai-plugin.json:", e)
else:
    print("Файл ai-plugin.json не найден в папке .well-known")

# Если папки или файла нет — прерываем запуск, чтобы не запускать сервер зря
if not os.path.exists(directory_path):
    raise FileNotFoundError(f"Directory {directory_path} does not exist")

# Монтируем папку .well-known как статические файлы
app.mount(
    "/.well-known",
    StaticFiles(directory=directory_path),
    name="well-known"
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

    import re
    match = re.search(r"v=([^&]+)", youtube_url)
    if not match:
        return {"summary": "Не удалось найти ID видео в ссылке"}

    video_id = match.group(1)

    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ru', 'en'])
    except Exception as e:
        return {"summary": f"Ошибка при получении транскрипта: {str(e)}"}

    full_text = " ".join([item['text'] for item in transcript])

    # Пример простого сокращения
    words = full_text.split()
    summary = " ".join(words[:100]) + "..." if len(words) > 100 else full_text

    return {"summary": summary}
