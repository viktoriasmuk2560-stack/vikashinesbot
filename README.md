# VikaShinesBot — Программа сияния

Готовый Telegram-бот на aiogram 3. Отвечает на «День 1»…«День 14», присылает видео, медитацию и задания.

## Как запустить локально (проще всего)
1. Установите Python 3.11+
2. `pip install -r requirements.txt`
3. Создайте в системе переменную окружения BOT_TOKEN со значением токена бота от @BotFather.
   - macOS/Linux: `export BOT_TOKEN=123:ABC`
   - Windows PowerShell: `$env:BOT_TOKEN="123:ABC"`
4. `python app.py`
5. В Telegram напишите боту: `День 1`

## Как заменить ссылки на видео/аудио
- В `content.json` поменяйте `url` на свои ссылки. Либо:
- Отправьте видео/аудио своему боту вручную 1 раз, получите `file_id` из `getUpdates` или логов, и вставьте вместо `url` поле `"file_id": "..."` — так файлы будут отправляться напрямую из Telegram без хостинга.

## Деплой (Render)
1. Создайте новый Web Service из репозитория проекта.
2. Python build, команда запуска: `python app.py`
3. В Settings → Environment задайте `BOT_TOKEN`.
4. Запустите. Используется long polling, вебхук не требуется.
