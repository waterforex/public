print("hello")
from telethon import TelegramClient

# Use your own values from my.telegram.org
api_id = 1445568
api_hash = '4835a86d74566a9338cb31fb0a4fef15'

# The first parameter is the .session file name (absolute paths allowed)
with TelegramClient('fishforex', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))