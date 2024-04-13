from AarohiX import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

EMOJI = [ ""
        ]

TAGMES = [ ""
        ]

@app.on_message(filters.command(["تاك", "all"], prefixes=["/", ""]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("- يمكنك استخدام هذا الامر في الجروبات و القنوات  .")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("- يمكن للمسؤول فقط استخدام هذا الامر  .")

    if message.reply_to_message and message.text:
        return await message.reply("- اكتب تاك + بالرد علي رساله .")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("- تاك + الرساله  .")
    else:
        return await message.reply("- تاك + الرساله  .")
    if chat_id in spam_chats:
        return await message.reply("- وقف عمليه التشغيل اولاً .")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(TAGMES)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@app.on_message(filters.command(["ايقاف تاك", ""], prefixes=["/", ""]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("- مفيش تاك شغال  .")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("- هذا الامر مخصص للمسؤولين فقط .")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("- توقف التاك .")
