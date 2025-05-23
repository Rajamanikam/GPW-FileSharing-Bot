# start.py

import os, asyncio, humanize
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, FILE_AUTO_DELETE
from helper_func import is_subscribed, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user

file_auto_delete = humanize.naturaldelta(FILE_AUTO_DELETE)


@Bot.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if subscribed
    if not await is_subscribed(None, client, message):
        buttons = [[InlineKeyboardButton("Join Channel", url=client.invitelink)]]
        if len(message.command) > 1:
            buttons.append([InlineKeyboardButton("🔁 Try Again", url=f"https://t.me/{client.username}?start={message.command[1]}")])
        await message.reply(
            text=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
        return

    # Register new user
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except Exception as e:
            print(f"Error adding user: {e}")

    # Handle /start with file argument
    if len(message.text) > 7:
        try:
            base64_string = message.text.split(" ", 1)[1]
            decoded = await decode(base64_string)
            args = decoded.split("-")
        except Exception as e:
            return await message.reply("Invalid start parameter.")

        try:
            if len(args) == 3:
                start = int(int(args[1]) / abs(client.db_channel.id))
                end = int(int(args[2]) / abs(client.db_channel.id))
                ids = list(range(start, end + 1)) if start <= end else list(range(start, end - 1, -1))
            elif len(args) == 2:
                ids = [int(int(args[1]) / abs(client.db_channel.id))]
            else:
                return await message.reply("Invalid start parameters.")
        except Exception as e:
            return await message.reply("Failed to decode file ID.")

        wait_msg = await message.reply("<b><i>📡 Please Wait...</i></b>")
        try:
            messages = await get_messages(client, ids)
        except:
            return await wait_msg.edit("<b><i>Something Went Wrong!</i></b>")

        await wait_msg.delete()
        sent_msgs = []
        for msg in messages:
            caption = ""
            if CUSTOM_CAPTION and msg.document:
                caption = CUSTOM_CAPTION.format(
                    previouscaption=msg.caption.html if msg.caption else "",
                    filename=msg.document.file_name
                )
            else:
                caption = msg.caption.html if msg.caption else ""

            try:
                new_msg = await msg.copy(
                    chat_id=message.chat.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=msg.reply_markup if DISABLE_CHANNEL_BUTTON else None,
                    protect_content=PROTECT_CONTENT
                )
                sent_msgs.append(new_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception as e:
                print(f"Error sending file: {e}")

        warn = await client.send_message(
            chat_id=message.chat.id,
            text=f"<b>⚠️ Files will be deleted in {file_auto_delete}. Please save to Saved Messages.</b>"
        )
        asyncio.create_task(delete_files(sent_msgs, client, warn))

    else:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("😊 About Me", callback_data="about"),
             InlineKeyboardButton("🔒 Close", callback_data="close")]
        ])
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )


async def delete_files(messages, client, notice_msg):
    await asyncio.sleep(FILE_AUTO_DELETE)
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"Failed to delete message {msg.id}: {e}")
    try:
        await notice_msg.edit_text("<b><i>✅ Files Deleted Successfully</i></b>")
    except:
        pass


@Bot.on_message(filters.command("users") & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    users = await full_userbase()
    await message.reply(f"{len(users)} users are using this bot.")


@Bot.on_message(filters.command("broadcast") & filters.private & filters.user(ADMINS))
async def broadcast(client: Bot, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")

    users = await full_userbase()
    total, success, blocked, deleted, failed = 0, 0, 0, 0, 0
    for user_id in users:
        try:
            await message.reply_to_message.copy(user_id)
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            success += 1
        except UserIsBlocked:
            await del_user(user_id)
            blocked += 1
        except InputUserDeactivated:
            await del_user(user_id)
            deleted += 1
        except:
            failed += 1
        total += 1

    summary = f"""<b>Broadcast Done ✅</b>
<b>Total:</b> {total}
<b>Success:</b> {success}
<b>Blocked:</b> {blocked}
<b>Deleted:</b> {deleted}
<b>Failed:</b> {failed}"""
    await message.reply(summary)

