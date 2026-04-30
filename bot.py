import os
import logging
import requests
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_music(query):
    url = f"https://itunes.apple.com/search?term={requests.utils.quote(query)}&media=music&limit=5&entity=song"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        results = []
        for item in data.get("results", []):
            results.append({
                "title": item.get("trackName", "Noma'lum"),
                "artist": item.get("artistName", "Noma'lum"),
                "duration": item.get("trackTimeMillis", 0) // 1000,
                "yt_query": f"{item.get('trackName','')} {item.get('artistName','')} audio"
            })
        return results
    except:
        return []

def format_duration(seconds):
    if not seconds:
        return "0:00"
    return f"{seconds//60}:{seconds%60:02d}"

async def start(update: Update, context):
    await update.message.reply_text(
        "Salom! 🎵\n\nQo'shiq nomini yozing — men topib yuklab beraman!\n\nMasalan: Janona yoki Adele Hello"
    )

async def handle_message(update: Update, context):
    query = update.message.text
    msg = await update.message.reply_text(f"🔍 {query} qidirilmoqda...")
    
    results = search_music(query)
    
    if not results:
        await msg.edit_text("❌ Topilmadi. Boshqa nom bilan qidiring.")
        return
    
    context.user_data["results"] = results
    
    text = f"🎵 '{query}' natijalari:\n\n"
    keyboard = []
    
    for i, track in enumerate(results):
        dur = format_duration(track["duration"])
        text += f"{i+1}. 🎵 {track['title']}\n    👤 {track['artist']}  ⏱ {dur}\n\n"
        keyboard.append([InlineKeyboardButton(
            f"⬇️ {i+1}. {track['title'][:30]}",
            callback_data=f"dl_{i}"
        )])
    
    keyboard.append([InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")])
    
    await msg.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_callback(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == "cancel":
        await query.edit_message_text("✅ Bekor qilindi.")
        return
    
    if query.data.startswith("dl_"):
        index = int(query.data[3:])
        results = context.user_data.get("results", [])
        
        if not results or index >= len(results):
            await query.edit_message_text("❌ Xatolik. Qaytadan qidiring.")
            return
        
        track = results[index]
        await query.edit_message_text(f"⏳ {track['title']} yuklanmoqda...")
        
        try:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": f"/tmp/{index}.%(ext)s",
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
                "quiet": True,
                "noplaylist": True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"ytsearch1:{track['yt_query']}"])
            
            mp3_file = f"/tmp/{index}.mp3"
            
            if os.path.exists(mp3_file):
                await query.edit_message_text(f"📤 {track['title']} yuborilmoqda...")
                with open(mp3_file, "rb") as f:
                    await context.bot.send_audio(
                        chat_id=query.message.chat_id,
                        audio=f,
                        title=track["title"],
                        performer=track["artist"],
                        caption=f"🎵 {track['title']}\n👤 {track['artist']}"
                    )
                os.remove(mp3_file)
                await query.edit_message_text("✅ Yuborildi!")
            else:
                await query.edit_message_text("❌ Yuklab bo'lmadi. Boshqa qo'shiq tanlang.")
        except Exception as e:
            logger.error(f"Download error: {e}")
            await query.edit_message_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()

if __name__ == "__main__":
    main()import os
import logging
import requests
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_music(query):
    url = f"https://itunes.apple.com/search?term={requests.utils.quote(query)}&media=music&limit=5&entity=song"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        results = []
        for item in data.get("results", []):
            results.append({
                "title": item.get("trackName", "Noma'lum"),
                "artist": item.get("artistName", "Noma'lum"),
                "duration": item.get("trackTimeMillis", 0) // 1000,
                "yt_query": f"{item.get('trackName','')} {item.get('artistName','')} audio"
            })
        return results
    except:
        return []

def format_duration(seconds):
    if not seconds:
        return "0:00"
    return f"{seconds//60}:{seconds%60:02d}"

async def start(update: Update, context):
    await update.message.reply_text(
        "Salom! 🎵\n\nQo'shiq nomini yozing — men topib yuklab beraman!\n\nMasalan: Janona yoki Adele Hello"
    )

async def handle_message(update: Update, context):
    query = update.message.text
    msg = await update.message.reply_text(f"🔍 {query} qidirilmoqda...")
    
    results = search_music(query)
    
    if not results:
        await msg.edit_text("❌ Topilmadi. Boshqa nom bilan qidiring.")
        return
    
    context.user_data["results"] = results
    
    text = f"🎵 '{query}' natijalari:\n\n"
    keyboard = []
    
    for i, track in enumerate(results):
        dur = format_duration(track["duration"])
        text += f"{i+1}. 🎵 {track['title']}\n    👤 {track['artist']}  ⏱ {dur}\n\n"
        keyboard.append([InlineKeyboardButton(
            f"⬇️ {i+1}. {track['title'][:30]}",
            callback_data=f"dl_{i}"
        )])
    
    keyboard.append([InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")])
    
    await msg.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_callback(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == "cancel":
        await query.edit_message_text("✅ Bekor qilindi.")
        return
    
    if query.data.startswith("dl_"):
        index = int(query.data[3:])
        results = context.user_data.get("results", [])
        
        if not results or index >= len(results):
            await query.edit_message_text("❌ Xatolik. Qaytadan qidiring.")
            return
        
        track = results[index]
        await query.edit_message_text(f"⏳ {track['title']} yuklanmoqda...")
        
        try:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": f"/tmp/{index}.%(ext)s",
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
                "quiet": True,
                "noplaylist": True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"ytsearch1:{track['yt_query']}"])
            
            mp3_file = f"/tmp/{index}.mp3"
            
            if os.path.exists(mp3_file):
                await query.edit_message_text(f"📤 {track['title']} yuborilmoqda...")
                with open(mp3_file, "rb") as f:
                    await context.bot.send_audio(
                        chat_id=query.message.chat_id,
                        audio=f,
                        title=track["title"],
                        performer=track["artist"],
                        caption=f"🎵 {track['title']}\n👤 {track['artist']}"
                    )
                os.remove(mp3_file)
                await query.edit_message_text("✅ Yuborildi!")
            else:
                await query.edit_message_text("❌ Yuklab bo'lmadi. Boshqa qo'shiq tanlang.")
        except Exception as e:
            logger.error(f"Download error: {e}")
            await query.edit_message_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()

if __name__ == "__main__":
    main()
