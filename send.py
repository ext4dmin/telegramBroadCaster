import os
import sys
import csv
import logging
from config import CHATS_CSV, LOG_PATH
from telegram_client import get_client
from db import add_message, get_unsent_messages, mark_sent

# Настройка логов
logging.basicConfig(
    filename=LOG_PATH,
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def prompt_yes_no_cancel(prompt: str) -> str:
    """Возвращает 'y', 'n' или 'c'."""
    ans = input(f"{prompt} (y/N/Cancel(c)): ").strip().lower()
    if ans == 'c': return 'c'
    return 'y' if ans == 'y' else 'n'


def interactive_input():
    # Шаг 1: желание рассылки
    while True:
        start = input('Желаете сделать рассылку? (y/N): ').strip().lower()
        if start != 'y':
            print('Выход из приложения.')
            sys.exit(0)

        # Шаг 2: ввод текста
        while True:
            text = input('Введите текст сообщения: ').strip()
            choice = prompt_yes_no_cancel(f"Текст: {text}\nПравильно?")
            if choice == 'c':
                break  # назад к шагу 1
            if choice == 'y':
                break  # далее
            # else: повтор ввода текста
        if choice == 'c':
            continue

        # Шаг 3: добавление изображения
        image_path = None
        while True:
            img_choice = prompt_yes_no_cancel('Добавить изображение?')
            if img_choice == 'c':
                break  # назад к шагу 1
            if img_choice == 'n':
                break  # без изображения
            # если 'y'
            while True:
                path = input('Укажите путь к изображению: ').strip()
                confirm = prompt_yes_no_cancel(f"Путь: {path}\nПравильно?")
                if confirm == 'c':
                    break  # назад к шагу 1
                if confirm == 'y':
                    image_path = path
                    break  # изображение подтверждено
                # else: запрашиваем путь снова
            if confirm == 'c':
                break
            # изображение либо загружено, либо отказ
            break
        if img_choice == 'c' or ('confirm' in locals() and confirm == 'c'):
            continue

        # Шаг 4: сохраняем в БД
        msg_id = add_message(text, image_path)
        logger.info(f"Сообщение {msg_id} сохранено в БД (изображение: {image_path})")
        print(f"Сообщение {msg_id} добавлено в очередь рассылки.")

        # Шаг 5: отправка всех неотправленных сообщений
        client = get_client()
        # читаем список чатов
        chats = []
        with open(CHATS_CSV, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                chats.append({'title': row['Название'], 'id': row['ИД']})
        logger.info('Начало рассылки сообщений.')

        for m_id, m_text, m_img in get_unsent_messages():
            for chat in chats:
                try:
                    if m_img:
                        client.loop.run_until_complete(
                            client.send_file(chat['id'], m_img, caption=m_text)
                        )
                    else:
                        client.loop.run_until_complete(
                            client.send_message(chat['id'], m_text)
                        )
                    logger.info(f"Сообщение {m_id} отправлено в '{chat['title']}' ({chat['id']})")
                except Exception as e:
                    logger.error(f"Ошибка при отправке {m_id} в '{chat['title']}': {e}")
            mark_sent(m_id)
            logger.info(f"Сообщение {m_id} помечено как отправленное.")

        print('Рассылка завершена.')
        sys.exit(0)

if __name__ == '__main__':
    interactive_input()