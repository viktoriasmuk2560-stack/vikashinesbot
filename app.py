import asyncio
import json
import logging
import os
from typing import Dict, Any

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Set BOT_TOKEN env var with your Telegram bot token")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Load content
with open("content.json", "r", encoding="utf-8") as f:
    CONTENT: Dict[str, Dict[str, Any]] = json.load(f)

def day_key_from_text(text: str) -> str | None:
    t = text.strip().lower().replace("ё", "е")
    if t.startswith("день "):
        part = t.split(" ", 1)[1]
        if part.isdigit():
            return f"day_{part}"
    # also allow /dayN commands like /day1
    if t.startswith("/day"):
        num = t[4:]
        if num.isdigit():
            return f"day_{num}"
    return None

@dp.message(CommandStart())
async def start(m: Message):
    await m.answer(
        "Привет! Я <b>Программа сияния</b> ✨\n"
        "Напиши, например: <b>День 1</b>, <b>День 2</b> ... <b>День 14</b>\n"
        "И я вышлю видео, медитацию и задания на день.\n\n"
        "Подсказки: /menu — список дней, /help — помощь"
    )

@dp.message(Command("help"))
async def help_cmd(m: Message):
    await m.answer("Напиши «День N» (например, День 1) или используй /menu, чтобы выбрать нужный день.")

@dp.message(Command("menu"))
async def menu(m: Message):
    days = sorted([int(k.split("_")[1]) for k in CONTENT.keys() if k.startswith("day_")])
    text = "Доступные дни:\n" + "\n".join(f"• День {d} — /day{d}" for d in days)
    await m.answer(text)

async def send_day(m: Message, key: str):
    data = CONTENT.get(key)
    if not data:
        await m.answer("Контент для этого дня пока не загружен.")
        return

    # Title/intro
    title = data.get("title", "").strip()
    intro = data.get("intro", "").strip()
    if title or intro:
        await m.answer(f"<b>{title}</b>\n{intro}".strip())

    # Video: prefer file_id, else URL as link
    vid = data.get("video", {})
    file_id = vid.get("file_id")
    url = vid.get("url")
    caption = vid.get("caption", "Видео тренировки")
    if file_id:
        try:
            await m.answer_video(video=file_id, caption=caption)
        except Exception as e:
            await m.answer(f"Не удалось отправить видео file_id. {e}")
    elif url:
        await m.answer(f"🎬 <b>Видео</b>: {url}\n{caption}")

    # Meditation: audio file_id or url + text
    med = data.get("meditation", {})
    m_file_id = med.get("file_id")
    m_url = med.get("url")
    m_caption = med.get("caption", "Медитация на день")
    if m_file_id:
        try:
            await m.answer_audio(audio=m_file_id, caption=m_caption, title="Meditation")
        except Exception as e:
            await m.answer(f"Не удалось отправить аудио file_id. {e}")
    elif m_url:
        await m.answer(f"🎧 <b>Медитация</b>: {m_url}\n{m_caption}")

    # Tasks / checklist
    tasks = data.get("tasks", [])
    if tasks:
        tasks_text = "\n".join([f"☑️ {t}" for t in tasks])
        await m.answer(f"<b>Задания дня:</b>\n{tasks_text}")

@dp.message(F.text)
async def day_router(m: Message):
    key = day_key_from_text(m.text or "")
    if key:
        await send_day(m, key)
    else:
        await m.answer("Напиши, например: <b>День 1</b>. Для списка команд — /menu.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
