import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8179944633:AAER7yxmwfUM8u99KaWUbY1IwmRWhtr54i4"
CHANNEL_USERNAME = "@shaxsiy_blog1o"
ADMIN_ID = 6733100026

bot = telebot.TeleBot(TOKEN)

waiting = []
active = {}

def main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Suhbatdosh topish", callback_data="find"),
        InlineKeyboardButton("Suhbatni to'xtatish", callback_data="stop"),
        InlineKeyboardButton("Bot haqida", callback_data="info"),
    )
    return markup

def is_subscribed(user_id):
    try:
        ch = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return ch.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start_handler(m):
    uid = m.from_user.id
    if not is_subscribed(uid):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
        bot.send_message(uid, "Botdan foydalanish uchun kanalga obuna bo'ling.", reply_markup=markup)
        return
    bot.send_message(uid, "Assalomu alaykum! 👋\nTugmalardan birini tanlang:", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    if not is_subscribed(uid):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
        bot.send_message(uid, "Botdan foydalanish uchun kanalga obuna bo'ling.", reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

    if call.data == "find":
        if uid in active:
            bot.send_message(uid, "Siz allaqachon suhbatdasiz. Suhbatni to'xtating.", reply_markup=main_menu())
        elif waiting and waiting[0] != uid:
            partner = waiting.pop(0)
            active[uid] = partner
            active[partner] = uid
            bot.send_message(uid, "✅ Suhbatdosh topildi!", reply_markup=main_menu())
            bot.send_message(partner, "✅ Suhbatdosh topildi!", reply_markup=main_menu())
        else:
            waiting.append(uid)
            bot.send_message(uid, "⏳ Kutish ro'yxatiga qo'shildingiz. Suhbatdosh topilishi bilan xabar beriladi.", reply_markup=main_menu())
    elif call.data == "stop":
        if uid in active:
            partner = active.pop(uid)
            active.pop(partner, None)
            bot.send_message(uid, "❌ Suhbat tugatildi.", reply_markup=main_menu())
            bot.send_message(partner, "❌ Suhbat tugatildi.", reply_markup=main_menu())
        elif uid in waiting:
            waiting.remove(uid)
            bot.send_message(uid, "❌ Kutish ro'yxatidan chiqarildingiz.", reply_markup=main_menu())
        else:
            bot.send_message(uid, "Sizda faol suhbat yo'q.", reply_markup=main_menu())
    elif call.data == "info":
        bot.send_message(uid, "Bu bot orqali anonim tarzda notanish odamlar bilan suhbatlasha olasiz.\n/start — menyu", reply_markup=main_menu())
    bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['text', 'photo', 'video', 'audio', 'document', 'voice', 'sticker'])
def relay_handler(m):
    uid = m.from_user.id
    if uid in active:
        partner = active[uid]
        if m.content_type == "text":
            bot.send_message(partner, m.text)
        elif m.content_type == "photo":
            bot.send_photo(partner, m.photo[-1].file_id, caption=m.caption or '')
        elif m.content_type == "video":
            bot.send_video(partner, m.video.file_id, caption=m.caption or '')
        elif m.content_type == "audio":
            bot.send_audio(partner, m.audio.file_id, caption=m.caption or '')
        elif m.content_type == "document":
            bot.send_document(partner, m.document.file_id, caption=m.caption or '')
        elif m.content_type == "voice":
            bot.send_voice(partner, m.voice.file_id)
        elif m.content_type == "sticker":
            bot.send_sticker(partner, m.sticker.file_id)
    else:
        bot.send_message(uid, "Sizda suhbatdosh yo‘q. Suhbat boshlash uchun tugmani bosing.", reply_markup=main_menu())

if __name__ == "__main__":
    bot.infinity_polling()
