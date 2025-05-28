from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME

_client = None

def get_client():
    """
    Инициализирует и возвращает синглтон TelegramClient.
    Первый запуск вызовет авторизацию (код из Telegram).
    """
    global _client
    if _client is None:
        _client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        _client.start()
    return _client