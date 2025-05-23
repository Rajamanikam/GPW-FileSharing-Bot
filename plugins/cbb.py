from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = (
                f"<b>🤖 <i>Bot Name:</i></b> <a href='https://t.me/GenieSourceCodeBot'><b><i>GenieSourceCodeBot</i></b></a>\n"
                f"<b>📝 <i>Language:</i></b> <a href='https://python.org'><b><i>Python 3</i></b></a>\n"
                f"<b>📚 <i>Library:</i></b> <a href='https://pyrogram.org'><b><i>Pyrogram {__version__}</i></b></a>\n"
                f"<b>🚀 <i>Server:</i></b> <a href='https://railway.app'><b><i>Railway</i></b></a>\n"
                f"<b>📢 <i>Channel:</i></b> <a href='https://t.me/GenieProjectsWorld'><b><i>Genie Projects World</i></b></a>\n"
                f"<b>🧑‍💻 <i>Developer:</i></b> <a href='tg://user?id={OWNER_ID}'><b><i>Rajamanikam</i></b></a>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data="close")]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

