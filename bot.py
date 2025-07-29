from telethon.sync import TelegramClient, events
import re, os

api_id = 6754402
api_hash = '4c15b31accaa22d775db7cf07e0caee1'
TARGET_CHANNEL = 1529739508

client = TelegramClient('my_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    text = event.raw_text
    m = re.search(r'(https://t\\.me/c/(\\d+)/(\\d+))', text)
    if m:
        try:
            ch_id = int("-100" + m.group(2))
            msg_id = int(m.group(3))
            msg = await client.get_messages(ch_id, ids=msg_id)
            if msg.file:
                path = await msg.download_media()
                await client.send_file(TARGET_CHANNEL, path, caption=msg.text or "")
                os.remove(path)
                await event.reply("✅ File uploaded!")
            elif msg.message:
                await client.send_message(TARGET_CHANNEL, msg.message)
                await event.reply("✅ Text posted!")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")

client.start()
print("🤖 Bot running — send t.me/c/... links now")
client.run_until_disconnected()
