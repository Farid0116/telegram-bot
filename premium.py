import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

# 🔑 Bot tokeni
TOKEN = "7805301069:AAHMZsHBAl1_li5nQF2g4oExMDplCCKpEy8"

# 🔹 Bot va dispatcher yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 📌 Narxlar ro‘yxati
prices = {
    "premium": [
        ("🎁 Telegram Premium", "1 oy", "46,000 so‘m", "price_premium_1month"),
        ("🎁 Telegram Premium", "3 oy", "170,000 so‘m", "price_premium_3month"),
    ],
    "stars": [
        ("⭐ Telegram Stars", "50 stars", "15,000 so‘m", "price_stars_50"),
        ("⭐ Telegram Stars", "100 stars", "30,000 so‘m", "price_stars_100"),
    ],
    "uc": [
        ("🎮 PUBG UC", "60 UC", "14,000 so‘m", "price_uc_60"),
        ("🎮 PUBG UC", "325 UC", "65,000 so‘m", "price_uc_325"),
    ]
}

# 📌 Narx tugmalarini yaratish
def generate_price_buttons(service):
    buttons = [[InlineKeyboardButton(text=f"{duration} - {price}", callback_data=callback)] for _, duration, price, callback in prices[service]]
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"back_to_{service}")])  # Xizmatga qaytarish
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 📌 Asosiy menyu
services_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🚀 Telegram Premium", callback_data="premium_service")],
    [InlineKeyboardButton(text="⭐ Telegram Stars", callback_data="stars_service")],
    [InlineKeyboardButton(text="🎮 PUBG UC", callback_data="uc_service")],
])

# 📌 To‘lov ma'lumotlarini chiqarish
def generate_payment_message(service, duration, price):
    return (f"✅ Siz tanlagan xizmat: {service}\n"
            f"⏳ Davomiyligi: {duration}\n"
            f"💰 Narxi: {price}\n\n"
            "📜 To‘lov uchun karta raqami: `9860 0366 0913 7041`\n"
            "📞 To‘lov qilganingizdan so‘ng adminga to‘lov chekini yuboring va tasdiqlashini kuting!"), InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="👤 Admin bilan bog‘lanish", url="https://t.me/Darkness_premium")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"back_to_{service}")]
            ])

# 📌 Xizmat tanlaganda narxlarni chiqarish
@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    if call.data == "premium_service":
        await call.message.edit_text("🚀 *Telegram Premium narxlari:*", reply_markup=generate_price_buttons("premium"), parse_mode="Markdown")
    
    elif call.data == "stars_service":
        await call.message.edit_text("⭐ *Telegram Stars narxlari:*", reply_markup=generate_price_buttons("stars"), parse_mode="Markdown")
    
    elif call.data == "uc_service":
        await call.message.edit_text("🎮 *PUBG UC narxlari:*", reply_markup=generate_price_buttons("uc"), parse_mode="Markdown")

    # 🔙 Xizmatning narxlar ro‘yxatiga qaytish
    elif call.data.startswith("back_to_"):
        service = call.data.split("_")[2]  # Xizmat nomini olish (premium, stars, uc)
        await call.message.edit_text(f"📌 *{service.capitalize()} narxlari:*", reply_markup=generate_price_buttons(service), parse_mode="Markdown")

    # 🔹 Narxni bosganda to‘lov ma'lumotlarini chiqarish
    else:
        for service, items in prices.items():
            for service_name, duration, price, callback in items:
                if call.data == callback:
                    text, keyboard = generate_payment_message(service_name, duration, price)
                    await call.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
                    break

    await call.answer()

# 📌 /start buyrug‘i
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("📌 *Xizmatlardan birini tanlang:*", reply_markup=services_menu, parse_mode="Markdown")

# 📌 Botni ishga tushirish
async def main():
    logging.info("Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
