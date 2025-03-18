import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN ='7805301069:AAHMZsHBAl1_li5nQF2g4oExMDplCCKpEy8'

# Log
logging.basicConfig(level=logging.INFO)

# Init
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Menu tugmalari ---
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)

menu_kb.add(KeyboardButton("🌟 Bepul Premium va Stars olish 🌟"))

menu_kb.row(
    KeyboardButton("💸 Premium Narxlar"), KeyboardButton("⭐ Stars Narxlari")
)

menu_kb.add(KeyboardButton("🏆 TOP Reyting"))

menu_kb.row(
    KeyboardButton("🎁 Bonus olish"), KeyboardButton("💳 Mening Hisobim")
)

menu_kb.row(
    KeyboardButton("📝 Qo'llanma"), KeyboardButton("👨‍💻 Administrator")
)

# /start handler
@dp.message_handler(commands=['start', 'menu'])
async def send_welcome(message: types.Message):
    await message.answer(
        "👋 <b>Salom, Darkness Service botiga xush kelibsiz!</b>\n\n"
        "💎 Bu yerda siz <b>Telegram Premium</b> xizmatini eng qulay narxlarda sotib olishingiz mumkin.\n\n"
        "⚡️ <b>Afzalliklar:</b>\n"
        "✅ Tez va ishonchli to‘lov\n"
        "✅ Sovg‘a sifatida yuborish imkoniyati\n"
        "✅ 100% kafolatlangan aktivatsiya\n\n"
        "📌 Premium narxlarini ko‘rish uchun menyudan foydalaning.\n\n"
        "🛒 <b>Buyurtma uchun admin:</b> @Darkness_premium", parse_mode="HTML", reply_markup=menu_kb
    )

# 💸 Premium Narxlar
@dp.message_handler(lambda message: message.text == "💸 Premium Narxlar")
async def premium_info(message: types.Message):
    photo = types.InputFile("/storage/emulated/0/Download/premium.jpg")
    text = (
    "<b>💸 Telegram Premium Narxlari</b>\n\n"
    "🔓 <b>Profilga kirish orqali:</b>\n"
    "◾ 1 oylik — 46.000 so'm\n"
    "◾ 12 oylik — 290.000 so'm\n\n"
    "🎁 <b>Gift sifatida olish:</b>\n"
    "◾ 3 oy — 170.000 so'm\n"
    "◾ 6 oy — 220.000 so'm\n"
    "◾ 12 oy — 400.000 so'm\n\n"
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
    "<b>⭐ Telegram Stars Narxlari</b>\n\n"
    "◾ 50 Stars — 15.000 so'm\n"
    "◾ 75 Stars — 20.000 so'm\n"
    "◾ 100 Stars — 30.000 so'm\n"
    "◾ 150 Stars — 50.000 so'm\n\n"
    "👨‍💻 <i>Admin bilan kelishilgan holda ko‘proq olish mumkin.</i>\n\n"
    "🛒 <b>Sotib olish uchun admin:</b> @Darkness_premium\n\n"
    "🔷 <i>Qadrdonlaringizga sovg‘a sifatida yuborish mumkin.</i>"
    )

    buy_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("⭐ Telegram Stars sotib olish", url="https://t.me/Darkness_premium")
    )

    await bot.send_photo(message.chat.id, photo, caption=text, reply_markup=buy_button, parse_mode="HTML")

@dp.message_handler(lambda message: message.text == "🌟 Bepul Premium va Stars olish 🌟")
async def referal_bonus(message: types.Message):
    referal_link = f"https://t.me/{(await bot.get_me()).username}?start={message.from_user.id}"
    
    text = (
        "<b>🎁 Sizga haligacha Telegram Premium sovg‘a qilishmadimi?</b>\n\n"
        "➖ <b>Telegram Premium</b> obunani sovg‘a sifatida tekinga olishni istaysizmi?\n\n"
        "Shunchaki pastdagi havola orqali do‘stlaringizni taklif qiling. Bot o‘zi sizga pul to‘laydi.\n"
        "To‘plangan pullarga Premium obunasini <b>follashtirish</b> mumkin.\n\n"
        f"👉 <b>Hoziroq o‘z sovg‘angiz sari olg‘a boring:</b> {referal_link}\n\n"
        "🔥 Do‘stlaringizni taklif qiling, sovg‘alarni oling!"
    )
    
    photo = types.InputFile("/storage/emulated/0/Download/premium.jpg")
    
    share_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("📩 Do‘stlarga Ulashish", switch_inline_query=referal_link)
    )

    await message.answer_photo(photo, caption=text, reply_markup=share_button, parse_mode="HTML")

# 👨‍💻 Admin
@dp.message_handler(lambda message: message.text == "👨‍💻 Administrator")
async def show_admin(message: types.Message):
    await message.answer("👨‍💻 Admin: @Darkness_premium")

# 🏆 TOP Reyting
@dp.message_handler(lambda message: message.text == "🏆 TOP Reyting")
async def top_reyting(message: types.Message):
    await message.answer("🏆 TOP Reyting: Coming soon...")

# 🎁 Bonus olish
@dp.message_handler(lambda message: message.text == "🎁 Bonus olish")
async def bonus_info(message: types.Message):
    await message.answer("🎁 <b>Bonus olish</b>\n\nBonus olish uchun quyidagi shartlarni bajaring:\n1. Do‘stlaringizni taklif qiling\n2. Faol bo‘ling\n3. Admin tavsiyasiga amal qiling.", parse_mode="HTML")

# 💳 Mening Hisobim
@dp.message_handler(lambda message: message.text == "💳 Mening Hisobim")
async def show_account(message: types.Message):
    await message.answer("💳 <b>Sizning hisobingiz</b>\n\n💰 Balans: 0 so'm\n🔓 Faol obuna: Mavjud emas.", parse_mode="HTML")

# 📝 Qo‘llanma
@dp.message_handler(lambda message: message.text == "📝 Qo'llanma")
async def show_guide(message: types.Message):
    await message.answer("📝 <b>Qo‘llanma</b>\n\nBotdan qanday foydalanish bo‘yicha to‘liq ko‘rsatma tez orada joylanadi.", parse_mode="HTML")

# Botni ishga tushirish
async def main():
    logging.info("Bot ishga tushdi!")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
