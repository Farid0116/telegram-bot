import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

# 🔑 Bot tokeni
TOKEN = "7805301069:AAHMZsHBAl1_li5nQF2g4oExMDplCCKpEy8"

# 🔹 Admin ma'lumotlari
ADMIN_URL = "https://t.me/Darkness_premium"
ADMIN_CARD_NUMBER = "9860 0366 0913 7041"

# 🔹 Bot va dispatcher yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 📌 Asosiy menyu
main_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="📌 Xizmatlar"), types.KeyboardButton(text="👨‍💼 Admin bilan bog‘lanish")],
        [types.KeyboardButton(text="✉️ Adminga murojaat xati")]
    ],
    resize_keyboard=True
)

# 📌 Xizmatlar menyusi
services_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🚀 Telegram Premium", callback_data="premium_service")],
    [InlineKeyboardButton(text="⭐ Telegram Stars", callback_data="stars_service")],
    [InlineKeyboardButton(text="🎮 PUBG UC", callback_data="uc_service")],
    [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="main_menu")]
])

# 📌 Narxlar ro‘yxati
prices = {
    "premium": [
        ("🎁 Telegram Premium", "1 oy", "46,000 so‘m", "price_premium_1month"),
        ("🎁 Telegram Premium", "3 oy", "170,000 so‘m", "price_premium_3month"),
        ("🎁 Telegram Premium", "6 oy", "220,000 so‘m", "price_premium_6month"),
        ("🎁 Telegram Premium", "1 yil", "400,000 so‘m", "price_premium_1year")
    ],
    "stars": [
        ("⭐ Telegram Stars", "50 stars", "15,000 so‘m", "price_stars_50"),
        ("⭐ Telegram Stars", "100 stars", "30,000 so‘m", "price_stars_100"),
        ("⭐ Telegram Stars", "500 stars", "115,000 so‘m", "price_stars_500")
    ],
    "uc": [
        ("🎮 PUBG UC", "60 UC", "14,000 so‘m", "price_uc_60"),
        ("🎮 PUBG UC", "325 UC", "65,000 so‘m", "price_uc_325"),
        ("🎮 PUBG UC", "660 UC", "125,000 so‘m", "price_uc_660")
    ]
}

# 📌 Narx tugmalarini yaratish
def generate_price_buttons(service):
    buttons = [[InlineKeyboardButton(text=f"{duration} - {price}", callback_data=callback)] for _, duration, price, callback in prices[service]]
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"back_to_prices_{service}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 📌 "⬅️ Orqaga" tugmasini bosganda narx menyusiga qaytarish
@dp.callback_query(F.data.startswith("back_to_prices_"))
async def back_to_price_list(call: CallbackQuery):
    service = call.data.replace("back_to_prices_", "")
    await call.message.edit_text(
        f"📌 {service.capitalize()} narxlari:",
        reply_markup=generate_price_buttons(service),
        parse_mode="Markdown"
    )

# 📌 Admin bilan bog‘lanish tugmasi
admin_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="👨‍💼 Admin bilan bog‘lanish", url=ADMIN_URL)]
])

# 📌 Narx tanlaganda chiqadigan tugma
def back_to_prices_button(service):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍💼 Admin bilan bog‘lanish", url=ADMIN_URL)],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"back_to_prices_{service}")]
    ])

# 📌 /start buyrug‘ini qayta ishlash
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("👋 Assalomu alaykum!\n\n📌 Xizmatlarni ko‘rish yoki 👨‍💼 admin bilan bog‘lanish uchun menyudan foydalaning:", reply_markup=main_menu)

# 📌 Asosiy menyu tugmalari
@dp.message(F.text == "📌 Xizmatlar")
async def show_services(message: types.Message):
    await message.answer("📌 *Xizmatlardan birini tanlang:*", reply_markup=services_menu, parse_mode="Markdown")

@dp.message(F.text == "👨‍💼 Admin bilan bog‘lanish")
async def contact_admin(message: types.Message):
    await message.answer("👨‍💼 *Admin bilan bog‘lanish uchun tugmani bosing:*", reply_markup=admin_button, parse_mode="Markdown")

# 📌 Xizmat tanlanganda narxlarni chiqarish
@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    if call.data == "premium_service":
        await call.message.edit_text("🚀 *Telegram Premium narxlari:*", reply_markup=generate_price_buttons("premium"), parse_mode="Markdown")
    
    elif call.data == "stars_service":
        await call.message.edit_text("⭐ *Telegram Stars narxlari:*", reply_markup=generate_price_buttons("stars"), parse_mode="Markdown")
    
    elif call.data == "uc_service":
        await call.message.edit_text("🎮 *PUBG UC narxlari:*", reply_markup=generate_price_buttons("uc"), parse_mode="Markdown")

    elif call.data.startswith("price_"):
        for service, items in prices.items():
            for name, duration, price, callback in items:
                if call.data == callback:
                    await call.message.edit_text(
                        f"✅ *Siz tanlagan xizmat:* {name}\n"
                        f"⏳ *Davomiyligi:* {duration}\n"
                        f"💰 *Narxi:* {price}\n\n"
                        f"📝 *To‘lov uchun karta raqami:* `{ADMIN_CARD_NUMBER}`\n\n"
                        "📞 *To‘lov qilganingizdan so‘ng adminga to‘lov chekini yuboring va tasdiqlashini kuting!*",
                        reply_markup=back_to_prices_button(service),
                        parse_mode="Markdown"
                    )
                    return

    elif call.data == "main_menu":
        await call.message.edit_text("📌 *Xizmatlardan birini tanlang:*", reply_markup=services_menu, parse_mode="Markdown")

    await call.answer()

# 📌 Botni ishga tushirish
async def main():
    logging.info("Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
