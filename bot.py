import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = '7338152003:AAEflY4nO79DXsY1xhnSf26xDd7DGiuZKR4'  # Telegram BotFather'dan olingan tokenni shu yerga kiriting

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Karta to'plami
deck = ['6♦', '6♣', '6♥', '6♠', '7♦', '7♣', '7♥', '7♠', '8♦', '8♣', '8♥', '8♠',
        '9♦', '9♣', '9♥', '9♠', '10♦', '10♣', '10♥', '10♠', 'J♦', 'J♣', 'J♥', 'J♠',
        'Q♦', 'Q♣', 'Q♥', 'Q♠', 'K♦', 'K♣', 'K♥', 'K♠', 'A♦', 'A♣', 'A♥', 'A♠']

# Foydalanuvchilar ma'lumotlarini saqlash
games = {}

# O'yinni boshlash uchun komandani qo'lga olish
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Durak o'yiniga xush kelibsiz. O'yinni boshlash uchun '/play' buyruqni kiriting!")

# O'yinni boshlash
@dp.message_handler(commands=['play'])
async def start_game(message: types.Message):
    user_id = message.from_user.id
    
    # O'yinchini ro'yxatga olish
    if user_id not in games:
        games[user_id] = {
            'deck': deck.copy(),
            'user_hand': [],
            'bot_hand': [],
            'trump_card': '',
            'turn': 'user',  # o'yinni kim boshlaydi
        }
        random.shuffle(games[user_id]['deck'])  # Karta to'plamini aralashtirish
        games[user_id]['trump_card'] = games[user_id]['deck'].pop()  # Kozir kartani olish
        await message.reply(f"O'yin boshlandi! Kozir karta: {games[user_id]['trump_card']}")
        
        # Kartalarni o'yinchilarga taqsimlash
        for _ in range(6):
            games[user_id]['user_hand'].append(games[user_id]['deck'].pop())
            games[user_id]['bot_hand'].append(games[user_id]['deck'].pop())
        
        await message.reply(f"Sizning qo'lingiz: {', '.join(games[user_id]['user_hand'])}")
        await bot_turn(message)

# Bot harakati
async def bot_turn(message):
    user_id = message.from_user.id
    
    if games[user_id]['turn'] == 'bot':
        bot_card = random.choice(games[user_id]['bot_hand'])
        games[user_id]['bot_hand'].remove(bot_card)
        games[user_id]['turn'] = 'user'
        await message.reply(f"Bot {bot_card} kartasini tashladi.")
        await message.reply(f"Sizning navbatingiz. Kartani tashlang yoki 'olaman' deb yozing.")
    else:
        await message.reply("Botning navbati emas.")

# O'yinchi harakati
@dp.message_handler(lambda message: True)
async def player_turn(message: types.Message):
    user_id = message.from_user.id
    if user_id not in games:
        await message.reply("Iltimos, o'yinni boshlash uchun '/play' buyruqni kiriting!")
        return

    user_input = message.text.upper()

    if user_input == 'OLAMAN':
        await message.reply("Siz kartalarni oldingiz. Endi botning navbati.")
        games[user_id]['turn'] = 'bot'
        await bot_turn(message)
        return

    if user_input in games[user_id]['user_hand']:
        games[user_id]['user_hand'].remove(user_input)
        await message.reply(f"Siz {user_input} kartasini tashladingiz. Botning navbati.")
        games[user_id]['turn'] = 'bot'
        await bot_turn(message)
    else:
        await message.reply("Qo'lingizda bunday karta yo'q!")

# O'yin tugashi
def check_winner(user_id):
    if not games[user_id]['user_hand']:
        return "Siz yutdingiz!"
    elif not games[user_id]['bot_hand']:
        return "Bot yutdi!"
    return None

# O'yin jarayonini kuzatish
@dp.message_handler(commands=['status'])
async def check_status(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in games:
        await message.reply("O'yin hali boshlanmadi. '/play' komandasi orqali o'yinni boshlang.")
        return

    user_hand = ', '.join(games[user_id]['user_hand'])
    bot_hand_count = len(games[user_id]['bot_hand'])
    
    await message.reply(f"Sizning qo'lingiz: {user_hand}")
    await message.reply(f"Botda {bot_hand_count} ta karta bor.")

# O'yinni tozalash
@dp.message_handler(commands=['reset'])
async def reset_game(message: types.Message):
    user_id = message.from_user.id
    
    if user_id in games:
        del games[user_id]
        await message.reply("O'yin tozalandi. Yangi o'yin boshlash uchun '/play' komandasini kiriting.")
    else:
        await message.reply("O'yin hali boshlanmadi.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)