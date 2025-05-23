import os
import logging
from logging.handlers import RotatingFileHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")

OWNER_ID = 7112455859
DB_URL = os.environ.get("DB_URL", "")
DB_NAME = "genieprojectsworld"

CHANNEL_ID = -1002236200390
FORCE_SUB_CHANNEL = -1002178375744

FILE_AUTO_DELETE = 0  # 0 means auto-delete is turned off

PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

try:
    ADMINS = [7112455859]  # Your Telegram ID as both admin and owner
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False
DISABLE_CHANNEL_BUTTON = True if os.environ.get('DISABLE_CHANNEL_BUTTON', "True") == "True" else False

BOT_STATS_TEXT = "<b>BOT UPTIME :</b>\n{uptime>"

USER_REPLY_TEXT = "<b><i>Please don't Send Me Messages Directly. I am just a File Sharing Bot 😄</i></b>"

START_MSG = os.environ.get("START_MESSAGE",
    "<b><i>Hi {mention} 👋\n\nWelcome to Genie Projects World Bot 🌐!\nI'm your permanent file store assistant.\nUse proper links shared in our channel to access your project files instantly.\n\nPowered by <a href='https://t.me/genieprojectsworld'>Genie Projects World</a></i></b>"
)

FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE",
    "<b><i>Hello {mention} 🌟\n\nTo access project files, please join our official channel first:\n<a href='https://t.me/genieprojectsworld_offl'>Genie Projects World</a>\n\nIt's free, and it helps you stay updated with our latest projects! 🚀</i></b>"
)

ADMINS.append(OWNER_ID)

LOG_FILE_NAME = "gpwfilesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
