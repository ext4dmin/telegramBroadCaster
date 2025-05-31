import os
from dotenv import load_dotenv

# Load vars from .env
load_dotenv()

API_ID = int(os.getenv('API_ID', ''))
API_HASH = os.getenv('API_HASH', '')
SESSION_NAME = os.getenv('SESSION_NAME', 'session')

# Path to files
CHATS_CSV = os.getenv('CHATS_CSV', 'chats.csv')
DB_PATH = os.getenv('DB_PATH', 'messages.db')
LOG_PATH = os.getenv('LOG_PATH', 'send.log')