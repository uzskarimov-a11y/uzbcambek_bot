import logging
import os
import re
import tempfile

import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN topilmadi. Render'ning Environment bo'limiga "
        "BOT_TOKEN nomli o'zgaruvchi qo'shing."
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

URL_PATTERN = re.compile(
    r"(https?://(?:www\.)?(?:instagram\.com|youtube\.com|youtu\.be)\S+)"
)

MAX_TELEGRAM_FILE_MB = 50  # Botlar uchun yuklash chegarasi (asosiy limit)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! 👋\n\n"
        "Menga Instagram yoki YouTube havolasini yuboring — "
        "videoni yuklab, shu yerga tashlab beraman.\n\n"
        "Eslatma: faqat o'zingizga tegishli yoki ochiq (public) "
        "kontentni yuklang, mualliflik huquqiga rioya qiling."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Shunchaki Instagram yoki YouTube havolasini yuboring.\n"
        f"Eslatma: {MAX_TELEGRAM_FILE_MB}MB dan katta videolarni bot yubora olmaydi."
    )


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    match = URL_PATTERN.search(text)

    if not match:
        await update.message.reply_text(
            "Instagram yoki YouTube havolasini yuboring."
        )
        return

    url = match.group(1)
    status_msg = await update.message.reply_text("⏳ Video yuklanmoqda...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        out_template = os.path.join(tmp_dir, "%(id)s.%(ext)s")
        ydl_opts = {
            "outtmpl": out_template,
            "format": "mp4/best",
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "max_filesize": MAX_TELEGRAM_FILE_MB * 1024 * 1024,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info)

            if not os.path.exists(filepath):
                await status_msg.edit_text(
                    "❌ Video topilmadi yoki hajmi juda katta "
                    f"(limit: {MAX_TELEGRAM_FILE_MB}MB)."
                )
                return

            file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
            if file_size_mb > MAX_TELEGRAM_FILE_MB:
                await status_msg.edit_text(
                    f"❌ Video juda katta ({file_size_mb:.1f}MB). "
                    f"Limit: {MAX_TELEGRAM_FILE_MB}MB."
                )
                return

            await status_msg.edit_text("📤 Yuborilmoqda...")
            with open(filepath, "rb") as video_file:
                await update.message.reply_video(
                    video=video_file,
                    caption=info.get("title", ""),
                )
            await status_msg.delete()

        except yt_dlp.utils.DownloadError as e:
            logger.error("Yuklab olishda xatolik: %s", e)
            await status_msg.edit_text(
                "❌ Videoni yuklab bo'lmadi. Havola noto'g'ri, "
                "video xususiy (private) yoki mavjud emas bo'lishi mumkin."
            )
        except Exception as e:
            logger.error("Kutilmagan xatolik: %s", e)
            await status_msg.edit_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Xatolik yuz berdi:", exc_info=context.error)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_error_handler(error_handler)

    logger.info("Bot ishga tushdi...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
