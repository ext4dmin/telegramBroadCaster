# telegramBroadCaster

[![CodeQL](https://github.com/ext4dmin/telegramBroadCaster/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/ext4dmin/telegramBroadCaster/actions/workflows/github-code-scanning/codeql)

<img src="https://github.com/user-attachments/assets/a978087e-ef3c-489b-a270-5d23a205d5d3" alt="telegramBradCaster" width="500"/>


## Description
telegramBroadCaster is a Python tool for broadcasting messages (with optional images) to multiple Telegram groups or channels. It uses Telethon and a local SQLite database to manage message queues and supports both interactive and automated (cron) operation. All configuration is handled via environment variables or a .env file.

## Getting Telegram API ID and API Hash
To work with the Telegram API as a client (for example, to read chats or send messages as a user), you need an API ID and API Hash from Telegram, not a bot token.

**Steps:**
1. Go to: https://my.telegram.org
2. Log in with your Telegram account (using a code sent via SMS or Telegram).
3. Go to the "API Development Tools" section.
4. Fill out the form:
    - Application title (any name)
    - Short description (any text)
    - URL (you can use http://localhost)
5. After submitting, you will receive:
    - `api_id`
    - `api_hash`
6. Use these credentials in your `.env` file. These are required for libraries like Telethon or Pyrogram.

## Step-by-step Usage Guide

### 1. Clone the Repository
```bash
git clone <repo_url>
cd telegram-broadcast/telegramBroadCaster
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root (next to `config.py`) with the following content:
```
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_NAME=your_session_name
DB_PATH=messages.db
CHATS_CSV=chats.csv
LOG_PATH=send.log
```
Replace `your_api_id`, `your_api_hash`, and `your_session_name` with your actual Telegram API credentials and desired session name.

### 5. Prepare the List of Chats
- Use `list_chats.py` to print all group/channel titles and IDs your account can access:
  ```bash
  python list_chats.py
  ```
- Copy the required chat IDs and add them to `chats.csv` in the following format:
  ```csv
  ИмяЧата,Название,ИД
  Test,Test,-4817298758
  ```

### 6. Add Messages to the Queue
You can add messages programmatically:
```python
from db import add_message
add_message('Your message text', 'optional_image_path.jpg')
```
Or use the interactive mode (see below).

### 7. Run the Broadcast Script
- **Interactive mode:**
  ```bash
  python send.py
  ```
  You will be prompted to enter message text, optionally attach an image, and confirm before sending.

- **Automated mode (for cron):**
  ```bash
  python send.py --auto
  ```
  All unsent messages in the database will be sent without prompts.

### 8. Check Logs
All actions and errors are logged to the file specified in `LOG_PATH` (default: `send.log`).

---
## How It Works
1. **Configuration:** Loads API keys and paths from `config.py` (which reads from `.env`).
2. **Initialization:** Connects to SQLite database and initializes the Telethon client.
3. **Interactive CLI:** In manual mode, prompts for message text and optional image, with confirmation and cancel options.
4. **Chat List:** Reads the list of target chats from `chats.csv`.
5. **Message Queue:** Fetches all unsent messages from the database.
6. **Sending:** For each message and each chat:
   - If `image_path` is set, sends the image with the message as a caption.
   - Otherwise, sends a text message.
   - Logs success or error for each attempt.
7. **Mark as Sent:** After attempting delivery, marks the message as sent in the database.
8. **Exit:** Script terminates after processing all messages.

---
## Notes
- Make sure your Telegram account is a member of all target groups/channels and has permission to send messages.
- For public channels, you may use the username (e.g., `@channelname`) instead of the numeric ID in `chats.csv`.
- The script will not resend messages already marked as sent.
- Use the interactive mode for manual control and testing; use automated mode for scheduled/cron jobs.
