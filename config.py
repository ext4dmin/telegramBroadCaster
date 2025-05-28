import os
from dotenv import load_dotenv

# Загружает переменные окружения из .env
load_dotenv()

API_ID = int(os.getenv('API_ID', ''))
API_HASH = os.getenv('API_HASH', '')
SESSION_NAME = os.getenv('SESSION_NAME', 'session')

# Пути к файлам
CHATS_CSV = os.getenv('CHATS_CSV', 'chats.csv')
DB_PATH = os.getenv('DB_PATH', 'messages.db')
LOG_PATH = os.getenv('LOG_PATH', 'send.log')