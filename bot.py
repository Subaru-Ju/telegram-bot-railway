#!/usr/bin/env python3
"""
🤖 Telegram Bot for Щитоград
Deployed on Railway from GitHub
"""

import os
import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, ChatMemberHandler, ContextTypes

# === НАСТРОЙКИ ===
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8426210135:AAEO9TuoSSKLUfKggv9pcJp5m3cOt_dAg3U")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "-1003566552914")
ADMIN_ID = os.environ.get("ADMIN_ID", "5252848020")

# === ЛОГИРОВАНИЕ ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# === ТЕКСТ ПРИВЕТСТВИЯ ===
WELCOME_TEXT = """Добро пожаловать 👋 

Рады видеть тебя в сообществе «Щитоград»

Мы — сообщество людей, прошедших через реалии передовой. Мы понимаем не понаслышке, что действительно нужно нашим бойцам в каждой конкретной ситуации и на каждом участке фронта.

Наша миссия — превратить вашу поддержку в точный, адресный и эффективный результат. Мы не просто собираем помощь — мы обеспечиваем ее грамотную логистику и гарантированную доставку по цепочке «потребность — сбор — адресат».

Присоединяйтесь к нашей команде. Любая помощь - бесценный вклад в общую Победу 💪 🇷🇺"""

# === ОБРАБОТЧИКИ ===
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие новых участников"""
    try:
        chat_member = update.chat_member
        old_status = chat_member.old_chat_member.status
        new_status = chat_member.new_chat_member.status
        
        if old_status in ['left', 'kicked'] and new_status == 'member':
            user = chat_member.new_chat_member.user
            
            if user.id == context.bot.id:
                logger.info("🤖 Бот добавлен в канал")
                return
            
            await context.bot.send_message(
                chat_id=chat_member.chat.id,
                text=f"👋 {user.first_name}, {WELCOME_TEXT}"
            )
            logger.info(f"✅ Приветствовал {user.first_name}")
            
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    await update.message.reply_text(
        "🤖 Бот для канала Щитоград\n"
        "📍 Хостинг: Railway + GitHub\n"
        "✅ Статус: Работает"
    )

# === ЗАПУСК ===
def main():
    """Основная функция"""
    print("🚀 Запуск бота...")
    
    if not BOT_TOKEN or BOT_TOKEN == "8426210135:AAEO9TuoSSKLUfKggv9pcJp5m3cOt_dAg3U":
        print("⚠️  ВНИМАНИЕ: Используется тестовый токен!")
        print("📝 Установите BOT_TOKEN в переменных окружения")
    
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))
        
        print("✅ Бот запущен!")
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"💥 Ошибка: {e}")

if __name__ == '__main__':
    main()