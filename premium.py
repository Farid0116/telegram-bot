import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

# 🔑 Bot tokeni
TOKEN = "7805301069:AAHMZsHBAl1_li5nQF2g4oExMDplCCKpEy8"

# 🔹 Admin sahifasi va karta raqami
ADMIN_URL = "https://t.me/Darkness_premium"
ADMIN_CARD_NUMBER = "9860 0366 0913 7041"

# 📌 Bot va Dispatcher yaratish
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
    [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="services_menu")]
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
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="services_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 📌 Admin bilan bog‘lanish tugmasi
admin_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="👨‍💼 Admin bilan bog‘lanish", url=ADMIN_URL)]
])

# 📌 Narx tanlanganda chiqadigan tugma
def back_to_prices_button(service):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍💼 Admin bilan bog‘lanish", url=ADMIN_URL)],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"back_to_{service}")]
    ])

# 📌 /start komandasi
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("👋 Assalomu alaykum!\n\n📌 Xizmatlarni ko‘rish yoki 👨‍💼 admin bilan bog‘lanish uchun menyudan foydalaning:", reply_markup=main_menu)

# 📌 Xizmatlar menyusini ko‘rsatish
@dp.message(F.text == "📌 Xizmatlar")
async def show_services(message: types.Message):
    await message.answer("📌 *Xizmatlardan birini tanlang:*", reply_markup=services_menu, parse_mode="Markdown")

# 📌 Admin bilan bog‘lanish
@dp.message(F.text == "👨‍💼 Admin bilan bog‘lanish")
async def contact_admin(message: types.Message):
    await message.answer("👨‍💼 *Admin bilan bog‘lanish uchun tugmani bosing:*", reply_markup=admin_button, parse_mode="Markdown")

# 📌 Xizmat tanlanganda narxlarni ko‘rsatish
@dp.callback_query(F.data.in_(["premium_service", "stars_service", "uc_service"]))
async def show_prices(call: CallbackQuery):
    service = call.data.replace("_service", "")
    service_names = {"premium": "🚀 Telegram Premium", "stars": "⭐ Telegram Stars", "uc": "🎮 PUBG UC"}
    await call.message.edit_text(f"{service_names[service]} *narxlari:*", reply_markup=generate_price_buttons(service), parse_mode="Markdown")

# 📌 Narx tanlanganda to‘lov ma’lumotini chiqarish
@dp.callback_query(F.data.startswith("price_"))
async def show_payment_details(call: CallbackQuery):
    selected_service = None
    selected_duration = None
    selected_price = None

    for service, items in prices.items():
        for name, duration, price, callback in items:
            if call.data == callback:
                selected_service = name
                selected_duration = duration
                selected_price = price
                break

    if not selected_service:
        await call.answer("Xatolik! Narx topilmadi.", show_alert=True)
        return

    duration_text = f"⏳ *Davomiyligi:* {selected_duration}" if "Premium" in selected_service else f"📦 *Miqdori:* {selected_duration}"

    await call.message.edit_text(
        f"✅ *Siz tanlagan xizmat:* {selected_service}\n"
        f"{duration_text}\n"
        f"💰 *Narxi:* {selected_price}\n\n"
        f"💳 *To‘lov uchun karta raqami:* `{ADMIN_CARD_NUMBER}`\n\n"
        "📞 *To‘lov qilganingizdan so‘ng adminga to‘lov chekini yuboring va tasdiqlashini kuting!*",
        reply_markup=back_to_prices_button(call.data.split("_")[1]),
        parse_mode="Markdown"
    )

# 📌 Orqaga tugmasi bosilganda xizmatlar menyusini qayta chiqarish
@dp.callback_query(F.data == "services_menu")
async def back_to_services(call: CallbackQuery):
    await call.message.edit_text("📌 *Xizmatlardan birini tanlang:*", reply_markup=services_menu, parse_mode="Markdown")

# 📌 Asosiy funksiya
async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Dispatcherga botni qo‘shish
    dp["bot"] = bot  # Aiogram 3.x uchun
    
    # Pollingni ishga tushirish
    await dp.start_polling(bot)

# 📌 Kodni ishga tushirish
if __name__ == "__main__":
    asyncio.run(main())
