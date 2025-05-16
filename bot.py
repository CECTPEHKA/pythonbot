import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

TOKEN = "7783228934:AAGspVfKFiqZzEbYmS8alZ07CIi1zzz-SD8"

def is_valid_phone(phone):
    return re.match(r"^(\+?38)?(0\d{9})$", phone)

def start(update: Update, context: CallbackContext):
    menu = [["Капучино", "Латте", "Американо"]]
    update.message.reply_text(
        "Оберіть каву:",
        reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True)
    )

def handle_order(update: Update, context: CallbackContext):
    coffee = update.message.text
    context.user_data['coffee'] = coffee
    update.message.reply_text("Введіть номер телефону (формат: 0501234567):")

def save_data(update: Update, context: CallbackContext):
    phone = update.message.text
    if not is_valid_phone(phone):
        update.message.reply_text("❌ Невірний формат! Спробуйте ще раз (наприклад: 0501234567)")
        return

    coffee = context.user_data.get('coffee', 'Невідомо')
    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(f"{coffee}, {phone}\n")
    
    update.message.reply_text(f"✅ Дякуємо! Ваше замовлення ({coffee}) прийнято.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex("^(Капучино|Латте|Американо)$"), handle_order))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, save_data))

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()