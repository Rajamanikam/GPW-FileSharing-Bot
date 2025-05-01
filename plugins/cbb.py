from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery



@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>🤖 <i>My Name :</i></b> <a href='https://t.me/NeonFilesBot'><b><i>NeonFilesBot</i></b></a> \n<b>📝 <i>Language :</i></b> <a href='https://python.org'><b><i>Python 3</i></b></a> \n<b>📚 <i>Library :</i></b> <a href='https://pyrogram.org'><b><i>Pyrogram {__version__}</i></b></a> \n<b>🚀 <i>Server :</i></b> <a href='https://heroku.com'><b><i>Heroku</i></b></a> \n<b>📢 <i>Channel :</i></b> <a href='https://t.me/NeonFiles'><b><i>NeonFiles</i></b></a> \n<b>🧑‍💻 <i>Developer :</i></b> <a href='tg://user?id={OWNER_ID}'><b><i>NeonAnurag</i></b></a>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass





# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
