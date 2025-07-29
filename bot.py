from telethon.sync import TelegramClient

api_id = 6754402
api_hash = '4c15b31accaa22d775db7cf07e0caee1'
bot_token = '8498828779:AAHM-L6mlG6JGpR7oOu4-NBQXGEJcwjxB-g'

client = TelegramClient('my_session', api_id, api_hash).start(bot_token=bot_token)
