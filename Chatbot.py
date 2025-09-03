import os
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# Environment variables
TOKEN = os.environ['TOKEN']
CHANNEL_USERNAME = os.environ.get('CHANNEL_USERNAME', '@shaxsiy_blog1o')
ADMIN_ID = int(os.environ.get('ADMIN_ID', 6733100026))

bot = telebot.TeleBot(TOKEN)
waiting = []
active = {}

# --- Flask (Render portni talab qiladi) ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running on Render!"

# --- Bot funksiyalari ---
def main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Suhbatdosh topish", callback_data="find"),
        InlineKeyboardButton("Suhbatni to'xtatish", callback_data="stop"),
        InlineKeyboardButton("Bot haqida", callback_data="about"),
    )
    return markup

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

@bot.message_handler(commands=['start'])
def start_handler(message):
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"))
        bot.send_message(message.chat.id, "Botdan foydalanish uchun kanalga obuna bo‘ling!", reply_markup=markup)
        return
    bot.send_message(message.chat.id, "Assalomu alaykum! Xush kelibsiz!\nSuhbatdosh topish uchun tugmani bosing.", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id

    if call.data == "find":
        if user_id in waiting or user_id in active:
            bot.answer_callback_query(call.id, "Siz allaqachon navbattasiz yoki suhbatdasiz!")
            return
        waiting.append(user_id)
        bot.send_message(call.message.chat.id, "Siz navbatga qo‘shildingiz. Suhbatdosh topilmoqda...")

        if len(waiting) >= 2:
            user1 = waiting.pop(0)
            user2 = waiting.pop(0)
            active[user1] = user2
            active[user2] = user1
            bot.send_message(user1, "✅ Suhbatdosh topildi! Suhbatni boshlang.")
            bot.send_message(user2, "✅ Suhbatdosh topildi! Suhbatni boshlang.")

    elif call.data == "stop":
        if user_id in active:
            partner_id = active.pop(user_id)
            active.pop(partner_id, None)
            bot.send_message(user_id, "❌ Suhbat to‘xtatildi.", reply_markup=main_menu())
            bot.send_message(partner_id, "❌ Suhbatdosh suhbatni to‘xtatdi.", reply_markup=main_menu())
        else:
            bot.send_message(user_id, "Siz hozircha hech kim bilan suhbatda emassiz.", reply_markup=main_menu())

    elif call.data == "about":
        bot.send_message(user_id, "Anonim chat-bot. Suhbatdoshingizni topish uchun 'Suhbatdosh topish' tugmasini bosing.")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def relay_message(message):
    user_id = message.from_user.id
    if user_id in active:
        partner_id = active[user_id]
        try:
            bot.send_message(partner_id, message.text)
        except Exception:
            bot.send_message(user_id, "⚠️ Xabar yuborib bo‘lmadi.")
    else:
        bot.send_message(user_id, "Siz hozircha suhbatda emassiz.\nSuhbatdosh topish uchun tugmani bosing.", reply_markup=main_menu())

# --- Botni boshqa oqimda ishga tushiramiz ---
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
