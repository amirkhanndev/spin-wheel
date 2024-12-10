from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Bosqichlar
LANGUAGE, NAME, LOCATION, PHONE = range(4)

# Ma'lumotlarni saqlash uchun bo'sh lug'at
user_data = {}

# Til bo'yicha tarjimalar
translations = {
    "O'zbek lotin": {
        "start": "Iltimos, tilni tanlang:",
        "name": "Ismingizni kiriting:",
        "location": "Yashash viloyati yoki shahringizni kiriting:",
        "phone": "Telefon raqamingizni kiriting yoki ulashing:",
        "thank_you": "Rahmat! Ma'lumotlaringiz saqlandi!",
    },
    "O'zbek krill": {
        "start": "Илтимос, тилни танланг:",
        "name": "Исмингизни киритинг:",
        "location": "Яшаш вилояти ёки шаҳарингизни киритинг:",
        "phone": "Телефон рақамингизни киритинг ёки улашинг:",
        "thank_you": "Рахмат! Маълумотларингиз сақланди!",
    },
    "Rus": {
        "start": "Пожалуйста, выберите язык:",
        "name": "Введите ваше имя:",
        "location": "Введите ваш город или область:",
        "phone": "Введите или поделитесь своим номером телефона:",
        "thank_you": "Спасибо! Ваши данные сохранены!",
    },
    "Eng": {
        "start": "Please select your language:",
        "name": "Enter your name:",
        "location": "Enter your city or region:",
        "phone": "Enter or share your phone number:",
        "thank_you": "Thank you! Your data has been saved!",
    },
}

# /start komandasi
def start(update: Update, context: CallbackContext) -> int:
    buttons = [
        ["O'zbek lotin", "O'zbek krill"],
        ["Rus", "Eng"]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    update.message.reply_text("Iltimos, tilni tanlang:", reply_markup=reply_markup)
    return LANGUAGE

# Tilni tanlash
def set_language(update: Update, context: CallbackContext) -> int:
    language = update.message.text
    user_data['language'] = language
    update.message.reply_text(translations[language]["name"])
    return NAME

# Ismni olish
def set_name(update: Update, context: CallbackContext) -> int:
    user_data['name'] = update.message.text
    language = user_data['language']
    update.message.reply_text(translations[language]["location"])
    return LOCATION

# Viloyat yoki shaharni olish
def set_location(update: Update, context: CallbackContext) -> int:
    user_data['location'] = update.message.text
    language = user_data['language']
    button = KeyboardButton(translations[language]["phone"], request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], one_time_keyboard=True)
    update.message.reply_text(translations[language]["phone"], reply_markup=reply_markup)
    return PHONE

# Telefon raqamni olish
def set_phone(update: Update, context: CallbackContext) -> int:
    if update.message.contact:
        user_data['phone'] = update.message.contact.phone_number
    else:
        user_data['phone'] = update.message.text
    
    language = user_data['language']
    update.message.reply_text(
        f"{translations[language]['thank_you']}\n\n"
        f"Til: {language}\n"
        f"Ism: {user_data['name']}\n"
        f"Shahar: {user_data['location']}\n"
        f"Telefon: {user_data['phone']}"
    )
    return ConversationHandler.END

# Bekor qilish funksiyasi
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Jarayon bekor qilindi.")
    return ConversationHandler.END

def main():
    # Tokenni bu yerga qo'shing
    updater = Updater("8140989674:AAERkKxQtwoI9NvAaNMZ125Q-9SjXpDlIB4")
    dispatcher = updater.dispatcher

    # Suhbat boshqaruvchisi
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [MessageHandler(Filters.text & ~Filters.command, set_language)],
            NAME: [MessageHandler(Filters.text & ~Filters.command, set_name)],
            LOCATION: [MessageHandler(Filters.text & ~Filters.command, set_location)],
            PHONE: [MessageHandler(Filters.contact | Filters.text & ~Filters.command, set_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
