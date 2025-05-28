import csv
import sys
import logging
from config import CHATS_CSV, LOG_PATH
from telegram_client import get_client
from db import get_unsent_messages, mark_sent

# Логирование
logging.basicConfig(
    filename=LOG_PATH,
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# CLI: подтверждение
from argparse import ArgumentParser
parser = ArgumentParser(description='Telegram Broadcast')
parser.add_argument('--auto', action='store_true', help='Запуск без подтверждения')
args = parser.parse_args()

if not args.auto:
    confirm = input('Начать рассылку (y/N)? ')
    if confirm.lower() != 'y':
        print('Отменено.')
        sys.exit(0)

# Чтение списка чатов
chats = []
with open(CHATS_CSV, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        chats.append({'title': row['Название'], 'id': row['ИД']})

# Получаем клиента
client = get_client()
logger.info('Запуск рассылки')

# Основной цикл рассылки
for msg_id, text, image_path in get_unsent_messages():
    for chat in chats:
        try:
            if image_path:
                client.loop.run_until_complete(
                    client.send_file(chat['id'], image_path, caption=text)
                )
            else:
                client.loop.run_until_complete(
                    client.send_message(chat['id'], text)
                )
            logger.info(f"Сообщение {msg_id} отправлено в '{chat['title']}' ({chat['id']})")
        except Exception as e:
            logger.error(f"Ошибка при отправке {msg_id} в '{chat['title']}': {e}")
    # Помечаем как отправленное
    mark_sent(msg_id)
    logger.info(f"Сообщение {msg_id} помечено как отправленное во все чаты")