from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask
from threading import Thread
import yt_dlp
import os

TOKEN = "8369591726:AAH2sAA_04SRroMcWzzDeNO6Yz3NF7iDIhU"

# Flask server (Render uchun)
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "✅ Instagram Bot ishga tushdi!"

def run_flask():
    web_app.run(host="0.0.0.0", port=8080)

# Telegram bot funksiyalari
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom!\nMenga Instagram havolasini yuboring 🎥")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "instagram.com" not in url:
        await update.message.reply_text("❌ Iltimos, faqat Instagram link yuboring.")
        return

    await update.message.reply_text("⏳ Yuklab olinmoqda...")

    try:
        os.makedirs("downloads", exist_ok=True)
        output_path = "downloads/video.mp4"

        ydl_opts = {
            "outtmpl": output_path,
            "format": "mp4/best",
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(video=open(output_path, "rb"), caption="✅ Tayyor!")

        os.remove(output_path)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Xatolik: {e}")

def main():
    # Flaskni fon rejimda ishlatamiz
    Thread(target=run_flask, daemon=True).start()

    # Telegram bot
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("✅ Bot polling orqali ishga tushdi.")
    app.run_polling()

if __name__ == "__main__":
    main()
