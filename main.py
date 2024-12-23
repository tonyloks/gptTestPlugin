from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
from fastapi.staticfiles import StaticFiles
import os
from youtube_transcript_api import YouTubeTranscriptApi
from starlette.responses import PlainTextResponse, FileResponse
from services.youtube_transcript_service import get_transcript



app = FastAPI(
    title="YouTube Summary Plugin",
    description="...",
    version="0.0.1",
    servers=[{"url": "https://gpttestplugin.onrender.com"}]  # <-- указываем реальный домен
)


# Путь к папке .well-known
directory_path = os.path.join(os.path.dirname(__file__), ".well-known")


# Создаём папку, если её нет
if not os.path.exists(directory_path):
    try:
        os.makedirs(directory_path)
        print(f"Папка '{directory_path}' успешно создана.")
    except Exception as e:
        print(f"Ошибка при создании папки: {e}")
else:
    print(f"Папка '{directory_path}' уже существует.")



# Проверяем, что в папке действительно лежит ai-plugin.json
file_path = os.path.join(directory_path, "ai-plugin.json")

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

    try:
        # Вызываем нашу функцию из youtube_transcript_service
        full_text = get_transcript(youtube_url, languages=['ru', 'en'])
        return {"summary": full_text}
    except Exception as e:
        return {"summary": f"Ошибка при получении транскрипта: {str(e)}"}


static_folder = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_folder, exist_ok=True)
app.mount(
    "/static",
    StaticFiles(directory=static_folder),
    name="static"
)
@app.get("/logo.png")
def get_logo():
    file_path = os.path.join(static_folder, "logo.png")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    else:
        return PlainTextResponse("Logo not found", status_code=404)

# 3. Создаем эндпоинт /terms
@app.get("/terms", response_class=PlainTextResponse)
def terms():
    return "Условия использования: тут ваш текст."