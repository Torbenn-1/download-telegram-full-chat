#!/usr/bin/env python3

import asyncio
import json
from pathlib import Path
from dateutil import tz
from telethon import TelegramClient, errors
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto

# --- CONFIG ---
SESSION_NAME = "tele_download_session"            
OUTPUT_DIR = Path("/run/media/nox/backup")        
API_ID = 12345678                                 
API_HASH = "0000000000000000000000000000000"     

# lista de chats para baixar
CHATS = [
    "https://t.me/chat1",
    "https://t.me/chat2",
]
# ----------------

def sanitize_filename(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in " ._-").strip()[:200] or "file"

async def download_chat(client, chat_input):
    try:
        entity = await client.get_entity(chat_input)
    except Exception as e:
        print(f"[ERRO] Não foi possível resolver o chat {chat_input}: {e}")
        return

    chat_name = getattr(entity, "username", None) or getattr(entity, "title", None) or str(getattr(entity, "id", "chat"))
    safe_chat_name = sanitize_filename(chat_name)
    base_path = OUTPUT_DIR / safe_chat_name
    media_path = base_path / "media"
    base_path.mkdir(parents=True, exist_ok=True)
    media_path.mkdir(parents=True, exist_ok=True)

    messages_file = base_path / "messages.jsonl"

    print(f"\n[+] Iniciando download do chat: {chat_name}")
    print(f"    Mensagens → {messages_file}")
    print(f"    Mídias    → {media_path}")

    counter = 0
    async with client:
        with messages_file.open("w", encoding="utf-8") as out:
            async for msg in client.iter_messages(entity, reverse=True):
                counter += 1
                meta = {
                    "id": msg.id,
                    "date": msg.date.astimezone(tz.tzlocal()).isoformat() if msg.date else None,
                    "sender_id": getattr(msg, "from_id", None).user_id if getattr(msg, "from_id", None) else None,
                    "text": (msg.message or "")[:10000],
                    "has_media": bool(msg.media),
                    "media_type": None,
                    "media_filename": None,
                }

                if msg.media:
                    try:
                        saved = await msg.download_media(file=media_path)
                    except Exception as e:
                        meta["media_error"] = str(e)
                        saved = None
                    if saved:
                        if isinstance(saved, (str, bytes)):
                            fn = Path(saved).name
                            meta["media_filename"] = fn
                        else:
                            meta["media_filename"] = None

                    if isinstance(msg.media, MessageMediaPhoto):
                        meta["media_type"] = "photo"
                    elif isinstance(msg.media, MessageMediaDocument):
                        meta["media_type"] = "document"
                    else:
                        meta["media_type"] = type(msg.media).__name__

                out.write(json.dumps(meta, ensure_ascii=False) + "\n")

                if counter % 100 == 0:
                    print(f"    {counter} mensagens processadas...")

    print(f"[✔] Finalizado: {counter} mensagens baixadas de {chat_name}\n")

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    for chat in CHATS:
        await download_chat(client, chat)

    await client.disconnect()
    print("Todos os chats foram processados.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")
