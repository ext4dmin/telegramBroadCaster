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
    """Returns 'y', 'n' or 'c'."""
    ans = input(f"{prompt} (y/N/Cancel(c)): ").strip().lower()
    if ans == 'c': return 'c'
    return 'y' if ans == 'y' else 'n'


def interactive_input():
    # Step 1: broadcast intent
    while True:
        start = input('Do you want to start a broadcast? (y/N): ').strip().lower()
        if start != 'y':
            print('Exiting application.')
            sys.exit(0)

        # Step 2: enter message text
        while True:
            text = input('Enter message text: ').strip()
            choice = prompt_yes_no_cancel(f"Text: {text}\nIs this correct?")
            if choice == 'c':
                break  # back to step 1
            if choice == 'y':
                break  # next
            # else: re-enter text
        if choice == 'c':
            continue

        # Step 3: add image
        image_path = None
        while True:
            img_choice = prompt_yes_no_cancel('Add an image?')
            if img_choice == 'c':
                break  # back to step 1
            if img_choice == 'n':
                break  # no image
            # if 'y'
            while True:
                path = input('Enter image path: ').strip()
                confirm = prompt_yes_no_cancel(f"Path: {path}\nIs this correct?")
                if confirm == 'c':
                    break  # back to step 1
                if confirm == 'y':
                    image_path = path
                    break  # image confirmed
                # else: re-enter path
            if confirm == 'c':
                break
            # image either loaded or declined
            break
        if img_choice == 'c' or ('confirm' in locals() and confirm == 'c'):
            continue

        # Step 4: save to DB
        msg_id = add_message(text, image_path)
        logger.info(f"Message {msg_id} saved to DB (image: {image_path})")
        print(f"Message {msg_id} added to broadcast queue.")

        # Step 5: send all unsent messages
        client = get_client()
        # read chat list
        chats = []
        with open(CHATS_CSV, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                chats.append({'title': row['Name'], 'id': int(row['ID'].strip())})
        logger.info('Starting message broadcast.')

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
                    logger.info(f"Message {m_id} sent to '{chat['title']}' ({chat['id']})")
                except Exception as e:
                    logger.error(f"Error sending {m_id} to '{chat['title']}': {e}")
            mark_sent(m_id)
            logger.info(f"Message {m_id} marked as sent.")

        print('Broadcast finished.')
        sys.exit(0)

if __name__ == '__main__':
    interactive_input()