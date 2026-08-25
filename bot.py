import logging
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
QWEN_URL = os.getenv("QWEN_URL", "https://qwen.ai")
CAMB_URL = os.getenv("CAMB_URL", "https://camb.ai")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN topilmadi. .env fayliga yoki cloud'ning Environment "
        "Variables bo'limiga BOT_TOKEN=... deb qo'shing."
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 Qwen rejimi", web_app=WebAppInfo(url=QWEN_URL))],
        [InlineKeyboardButton("🎙 Camb rejimi", web_app=WebAppInfo(url=CAMB_URL))],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! 👋\n\n"
        "Bu bot orqali Qwen.ai va Camb.ai xizmatlariga ulanishingiz mumkin.\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=main_keyboard(),
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Komandalar:\n"
        "/start - Asosiy menyu\n"
        "/qwen - Qwen.ai ni ochish\n"
        "/camb - Camb.ai ni ochish\n"
        "/help - Yordam"
    )


async def qwen_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🤖 Qwen.ai ochish", web_app=WebAppInfo(url=QWEN_URL))]])
    await update.message.reply_text("Qwen.ai rejimi tanlandi:", reply_markup=kb)


async def camb_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🎙 Camb.ai ochish", web_app=WebAppInfo(url=CAMB_URL))]])
    await update.message.reply_text("Camb.ai rejimi tanlandi:", reply_markup=kb)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Xatolik yuz berdi:", exc_info=context.error)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("qwen", qwen_cmd))
    app.add_handler(CommandHandler("camb", camb_cmd))
    app.add_error_handler(error_handler)

    logger.info("Bot ishga tushdi...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
