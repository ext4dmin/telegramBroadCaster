from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def print_group_ids():
    await client.start()
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            title = dialog.title or '(без названия)'
            chat_id = dialog.id
            print(f'{title}: {chat_id}')

with client:
    client.loop.run_until_complete(print_group_ids())
