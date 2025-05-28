# telegramBroadCaster

## Описание
Скрипт `send.py` рассылает сообщения из SQLite БД в группы Telegram по списку из `chats.csv`.

## Установка
1. `git clone ...`
2. `cd telegram_broadcast`
3. `python3 -m venv venv && source venv/bin/activate`
4. `pip install -r requirements.txt`
5. Создать `.env` рядом с `config.py` (см. пример выше).

## Добавление сообщений
В Python:
```python
from db import add_message
add_message('Текст с эмодзи 😊', 'images/photo.jpg')
```

## Запуск рассылки

- Ручной: python send.py

- Автоматически (cron): python send.py --auto

Логи сохраняются в send.log.

---
## Алгоритм работы
1. **Конфиг**: загрузка API-ключей и путей из `config.py` (`.env`).
2. **Инициализация**: создаётся/подключается SQLite БД и Telethon-клиент.
3. **CLI**: при ручном запуске спрашивает подтверждение.
4. **Чтение**: парсинг `chats.csv` списка групп.
5. **Выбор**: получение всех `unsent_messages` из БД.
6. **Отправка**: для каждого сообщения и каждого чата:
   - если есть `image_path`, используется `send_file` с `caption=text`
   - иначе `send_message`
   - логирование успеха или ошибки в `send.log`
7. **Обновление**: после попыток отправки пометка `sent=1` у сообщения.
8. **Завершение**: скрипт выходит.