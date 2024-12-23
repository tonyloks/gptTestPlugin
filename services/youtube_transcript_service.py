import re
from typing import List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
from icecream import ic  # Подключаем icecream для логирования

# Настраиваем icecream (можно указать, какой вид сообщений вы хотите)
ic.configureOutput(includeContext=True)  # Включаем контекст (имя файла, строка)

def get_video_id(url: str) -> str:
    """
    Извлекает из ссылки на YouTube (в любом популярном формате) ID видео.
    Учитывает варианты:
      - https://youtu.be/<video_id>
      - https://www.youtube.com/watch?v=<video_id>
      - https://www.youtube.com/live/<video_id>
      - https://www.youtube.com/embed/<video_id>
      - https://www.youtube.com/v/<video_id>

    Пример:
      - https://youtu.be/cv1F_c66utw?si=8WhZS5G95PU9IqAD
      - https://www.youtube.com/watch?v=cv1F_c66utw
      - https://www.youtube.com/live/1yLUzSJe5bY?si=emPv_DAQk6Gr6oms

    Возвращает:
      - ID ролика (строка вида "cv1F_c66utw").

    Бросает ValueError, если ID найти не удалось.
    """
    ic(f"Пытаемся извлечь video_id из URL: {url}")  # Логируем входной URL

    pattern = (
        r"(?:youtu\.be/"         # короткая ссылка:  youtu.be/
        r"|youtube\.com/(?:watch\?v=|embed/|v/|live/)" # длинные ссылки: youtube.com/(watch?v=|embed/|v/|live/)
        r"|v=)"                  # возможно, строка напрямую начинается с '?v='
        r"([\w\-]{10,})"         # сам video_id (10 и более символов, если хотите, можно поставить {11,})
    )

    match = re.search(pattern, url)
    if match:
        video_id = match.group(1)
        ic(f"Найден video_id: {video_id}")  # Логируем найденный video_id
        return video_id
    else:
        error_message = f"Не удалось найти ID в ссылке: {url}"
        ic(error_message)  # Логируем ошибку
        raise ValueError(error_message)


def get_transcript(youtube_url: str, languages: List[str] = None) -> str:
    """
    Получает транскрипт из YouTube, используя `YouTubeTranscriptApi`.
    Внутри себя вызывает `get_video_id` для извлечения ID из ссылки.

    :param youtube_url: Полная ссылка на видео (short/long)
    :param languages: Предпочтительные языки ['ru','en'] и т.д.
    :return: Полный текст транскрипта одной строкой
    """
    ic(f"Начинаем обработку YouTube URL: {youtube_url}")  # Логируем входной URL

    if not languages:
        languages = ["ru", "en"]

    try:
        # Вызываем нашу функцию для извлечения ID
        video_id = get_video_id(youtube_url)
        ic(f"Получение транскрипта для video_id: {video_id}")  # Логируем ID видео

        # Получаем транскрипт
        transcript_data: List[Dict[str, str]] = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=languages
        )
        ic(f"Транскрипт успешно получен. Количество частей: {len(transcript_data)}")  # Логируем результат

        # Склеиваем все кусочки текста
        full_text = " ".join([item['text'] for item in transcript_data])
        ic(f"Общая длина транскрипта: {len(full_text)} символов")  # Логируем длину результата
        return full_text
    except Exception as e:
        error_message = f"Ошибка при получении транскрипта: {str(e)}"
        ic(error_message)  # Логируем ошибку
        raise RuntimeError(error_message)


if __name__ == "__main__":
    test_long_video = "https://www.youtube.com/live/1yLUzSJe5bY?si=emPv_DAQk6Gr6oms"

    ic("Тестируем get_transcript с длинной трансляцией")
    try:
        transcript = get_transcript(test_long_video)
        ic(f"Длина транскрипта: {len(transcript)} символов")
    except Exception as e:
        ic(f"Произошла ошибка: {str(e)}")
