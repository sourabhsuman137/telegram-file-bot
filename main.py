import os
import json
import asyncio
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError
from keep_alive import keep_alive

keep_alive()

api_id = 6754402
api_hash = '4c15b31accaa22d775db7cf07e0caee1'
phone_number = '+919709736704'

source_channel = -1002686762088
destination_channel = -1001529739508

session_name = 'my_session'
progress_file = 'processed_files.json'
download_folder = 'downloads'

os.makedirs(download_folder, exist_ok=True)

if os.path.exists(progress_file):
    with open(progress_file, 'r') as f:
        processed_ids = set(json.load(f))
else:
    processed_ids = set()

client = TelegramClient(session_name, api_id, api_hash)

async def process_files():
    try:
        await client.start(phone=phone_number)
        print("✅ Client connected successfully")

        count = 0
        async for message in client.iter_messages(source_channel):
            if message.id in processed_ids:
                continue

            if message.file and message.file.size <= 2 * 1024 * 1024 * 1024:
                file_name = f"file_{message.id}_{message.file.name or 'unknown'}"
                file_path = os.path.join(download_folder, file_name)
                try:
                    print(f"⬇️ Downloading: {file_name}")
                    await client.download_media(message, file_path)

                    print(f"⬆️ Uploading: {file_name}")
                    await client.send_file(destination_channel, file_path, caption=f"📎 From Source (ID: {message.id})")
                    print(f"✅ Uploaded and deleting local file")
                    os.remove(file_path)

                    processed_ids.add(message.id)
                    with open(progress_file, 'w') as f:
                        json.dump(list(processed_ids), f)

                    count += 1
                    print(f"✔️ Processed {count} files. Sleeping 2s...")
                    await asyncio.sleep(2)

                except FloodWaitError as e:
                    print(f"🚫 Flood wait: sleeping for {e.seconds} seconds...")
                    await asyncio.sleep(e.seconds + 5)
                except Exception as e:
                    print(f"❌ Error in message {message.id}: {e}")
            else:
                print(f"⏭️ Skipped message {message.id}: No file or file too large")

    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        await client.disconnect()
        print("📴 Client disconnected")

asyncio.run(process_files())