from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread
import yt_dlp
import os

# Token (Render'da Environment Variables orqali saqlash tavsiya etiladi)
TOKEN = "8369591726:AAH2sAA_04SRroMcWzzDeNO6Yz3NF7iDIhU"

# Flask server - Render uchun keep-alive
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Instagram bot ishga tushdi ✅"

def run_flask():
    web_app.run(host="0.0.0.0", port=8080)

# Telegram buyruqlar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom 👋\nMenga Instagram video linkini yuboring 🎥")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    # URL Instagramdanmi?
    if "instagram.com" not in url:
        await update.message.reply_text("❌ Iltimos, faqat Instagram video havolasini yuboring.")
        return

    await update.message.reply_text("⏳ Video yuklab olinmoqda, biroz kuting...")

    try:
        # Fayl nomini dinamik beramiz
        output_path = "downloads/video.mp4"
        os.makedirs("downloads", exist_ok=True)

        ydl_opts = {
            'outtmpl': output_path,
            'format': 'mp4/best',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Foydalanuvchiga video jo‘natamiz
        with open(output_path, "rb") as video:
            await update.message.reply_video(video=video, caption="✅ Yuklab olindi!")

        # Faylni o‘chiramiz
        os.remove(output_path)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Xatolik yuz berdi:\n`{e}`")

def main():
    # Flask serverni ishga tushuramiz (fon rejimda)
    Thread(target=run_flask).start()

    # Telegram botni ishga tushiramiz
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("✅ Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
