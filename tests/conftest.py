# Добавляем корневой каталог проекта в sys.path и задаём пустые переменные окружения для config
import sys
import os

# Вставляем корень проекта в sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Обеспечиваем, чтобы при импорте config.env были хоть какие-то значения
os.environ.setdefault('API_ID', '0')
os.environ.setdefault('API_HASH', 'hash')
os.environ.setdefault('SESSION_NAME', 'session')
os.environ.setdefault('CHATS_CSV', 'chats.csv')
os.environ.setdefault('DB_PATH', 'messages.db')
os.environ.setdefault('LOG_PATH', 'send.log')
