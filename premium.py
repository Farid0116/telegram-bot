
import asyncio
import logging
import json
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '7805301069:AAHMZsHBAl1_li5nQF2g4oExMDplCCKpEy8'

# Log
logging.basicConfig(level=logging.INFO)

# Init
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Referal fayl
REF_FILE = Path("referals.json")
if not REF_FILE.exists():
    with open(REF_FILE, "w") as f:
        json.dump({}, f)

# --- Menu tugmalari ---
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.add(KeyboardButton("🌟 Bepul Premium va Stars olish 🌟"))
menu_kb.row(KeyboardButton("💸 Premium Narxlar"), KeyboardButton("⭐ Stars Narxlari"))
menu_kb.add(KeyboardButton("🏆 TOP Reyting"))
menu_kb.row(KeyboardButton("🎁 Bonus olish"), KeyboardButton("💳 Mening Hisobim"))
menu_kb.row(KeyboardButton("📝 Qo'llanma"), KeyboardButton("👨‍💻 Administrator"))

# --- Referal funksiyalar ---
def add_referral(referrer_id, new_user_id):
    with open(REF_FILE, "r") as f:
        data = json.load(f)

    referrer_id = str(referrer_id)
    new_user_id = str(new_user_id)

    if referrer_id == new_user_id:
        return  # o'zini taklif qilolmaydi

    if referrer_id not in data:
        data[referrer_id] = {"invited": [], "balance": 0}

    if new_user_id not in data[referrer_id]["invited"]:
        data[referrer_id]["invited"].append(new_user_id)
        data[referrer_id]["balance"] += 300

        with open(REF_FILE, "w") as f:
            json.dump(data, f)

def get_balance(user_id):
    with open(REF_FILE, "r") as f:
        data = json.load(f)
    user_data = data.get(str(user_id), {"balance": 0})
    return user_data["balance"]

# --- /start handler
@dp.message_handler(commands=['start', 'menu'])
async def send_welcome(message: types.Message):
    args = message.get_args()
    if args.isdigit():
        add_referral(int(args), message.from_user.id)

    await message.answer(
        "👋 <b>Salom, Darkness Service botiga xush kelibsiz!</b>

"
        "💎 Bu yerda siz <b>Telegram Premium</b> xizmatini eng qulay narxlarda sotib olishingiz mumkin.

"
        "⚡️ <b>Afzalliklar:</b>
"
        "✅ Tez va ishonchli to‘lov
"
        "✅ Sovg‘a sifatida yuborish imkoniyati
"
        "✅ 100% kafolatlangan aktivatsiya

"
        "📌 Premium narxlarini ko‘rish uchun menyudan foydalaning.

"
        "🛒 <b>Buyurtma uchun admin:</b> @Darkness_premium", parse_mode="HTML", reply_markup=menu_kb
    )

# 💸 Premium Narxlar
@dp.message_handler(lambda message: message.text == "💸 Premium Narxlar")
async def premium_info(message: types.Message):
    photo = types.InputFile("/storage/emulated/0/Download/premium.jpg")
    text = (
        "<b>💸 Telegram Premium Narxlari</b>

"
        "🔓 <b>Profilga kirish orqali:</b>
"
        "◾ 1 oylik — 46.000 so'm
"
        "◾ 12 oylik — 290.000 so'm

"
        "🎁 <b>Gift sifatida olish:</b>
"
        "◾ 3 oylik — 170.000 so'm
"
        "◾ 6 oylik — 220.000 so'm
"
        "◾ 12 oylik — 400.000 so'm

"
        "🔷 <i>Qadrdonlaringizga hadya qilishingiz mumkin.</i>"
    )
    buy_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("⭐ Premium sotib olish", url="https://t.me/Darkness_premium")
    )
    await bot.send_photo(message.chat.id, photo, caption=text, reply_markup=buy_button, parse_mode="HTML")

# ⭐ Stars Narxlari
@dp.message_handler(lambda message: message.text == "⭐ Stars Narxlari")
async def stars_info(message: types.Message):
    photo = types.InputFile("/storage/emulated/0/Download/stars.jpg")
    text = (
        "<b>⭐ Telegram Stars Narxlari</b>

"
        "◾ 50 Stars — 15.000 so'm
"
        "◾ 75 Stars — 20.000 so'm
"
        "◾ 100 Stars — 30.000 so'm
"
        "◾ 150 Stars — 50.000 so'm

"
        "👨‍💻 <i>Admin bilan kelishilgan holda ko‘proq olish mumkin.</i>

"
        "🛒 <b>Sotib olish uchun admin:</b> @Darkness_premium

"
        "🔷 <i>Qadrdonlaringizga sovg‘a sifatida yuborishingiz mumkin.</i>"
    )
    buy_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("⭐ Telegram Stars sotib olish", url="https://t.me/Darkness_premium")
    )
    await bot.send_photo(message.chat.id, photo, caption=text, reply_markup=buy_button, parse_mode="HTML")

# 🌟 Bepul Premium va Stars olish 🌟
@dp.message_handler(lambda message: message.text == "🌟 Bepul Premium va Stars olish 🌟")
async def referal_bonus(message: types.Message):
    referal_link = f"https://t.me/{(await bot.get_me()).username}?start={message.from_user.id}"
    text = (
        "<b>🎁 Sizga haligacha Telegram Premium sovg‘a qilishmadimi?</b>

"
        "➖ <b>Telegram Premium</b> obunani sovg‘a sifatida tekinga olishni istaysizmi?

"
        "Do‘stlaringizni taklif qiling. Har bir do‘stingiz uchun <b>300 so‘m</b> bonus oling.

"
        f"<b>Referal havolangiz:</b> {referal_link}

"
        "🔥 Do‘stlaringizni taklif qiling, sovg‘alarni oling!"
    )
    photo = types.InputFile("/storage/emulated/0/Download/premium.jpg")
    share_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("📩 Do‘stlarga Ulashish", switch_inline_query=referal_link)
    )
    await message.answer_photo(photo, caption=text, reply_markup=share_button, parse_mode="HTML")

# 💳 Mening Hisobim
@dp.message_handler(lambda message: message.text == "💳 Mening Hisobim")
async def show_account(message: types.Message):
    bonus = get_balance(message.from_user.id)
    await message.answer(f"💳 <b>Sizning hisobingiz</b>

💰 Balans: {bonus} so'm
🔓 Faol obuna: Mavjud emas.", parse_mode="HTML")

# Qolgan tugmalar...
@dp.message_handler(lambda m: m.text == "👨‍💻 Administrator")
async def show_admin(message: types.Message):
    await message.answer("👨‍💻 Admin: @Darkness_premium")

@dp.message_handler(lambda m: m.text == "🏆 TOP Reyting")
async def top_reyting(message: types.Message):
    await message.answer("🏆 TOP Reyting: Coming soon...")

@dp.message_handler(lambda m: m.text == "🎁 Bonus olish")
async def bonus_info(message: types.Message):
    await message.answer("🎁 <b>Bonus olish</b>

Do‘stlaringizni taklif qiling va bonuslarni to‘plang!", parse_mode="HTML")

@dp.message_handler(lambda m: m.text == "📝 Qo'llanma")
async def show_guide(message: types.Message):
    await message.answer("📝 <b>Qo‘llanma</b>

Tez orada qo‘llanma joylanadi.", parse_mode="HTML")

# Run bot
async def main():
    logging.info("Bot ishga tushdi!")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
