from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "8369591726:AAH2sAA_04SRroMcWzzDeNO6Yz3NF7iDIhU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Menga Instagram video linkini yuboring 🎥")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("⏳ Yuklab olinmoqda...")
    try:
        ydl_opts = {
            'outtmpl': 'video.mp4',
            'format': 'mp4/best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await update.message.reply_video(video=open("video.mp4", "rb"))
    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

app.run_polling()
