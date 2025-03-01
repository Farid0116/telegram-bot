import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

# 🔑 Bot tokeni
TOKEN = "7805301069:AAHMZsHBAl1_li5nQF2g4oExMDplCCKpEy8"

# 🔹 Admin sahifasi va karta raqami
ADMIN_URL = "https://t.me/Darkness_premium"
ADMIN_CARD_NUMBER = "9860 0366 0913 7041"
ADMIN_ID = 734940228
GROUP_ID = -1002208256136

# 🔹 Bot va dispatcher
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
    [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")]
])

# 📌 Har 10 daqiqada guruhga xabar yuborish
async def send_scheduled_message():
    while True:
        try:
            text = (
                "🔥 *TELEGRAM PREMIUM – CHEGIRMALI NARXLAR!* 🔥\n\n"
                "🎁 *1 oy* – 46,000 so‘m\n"
                "🎁 *3 oy* – 170,000 so‘m\n"
                "🎁 *6 oy* – 220,000 so‘m\n"
                "🎁 *1 yil* – 400,000 so‘m\n\n"
                "✅ *Reklamalarsiz foydalaning!*\n"
                "✅ *Eksklyuziv sticker va emojilar!*\n"
                "✅ *Tezkor yuklab olish!*\n"
                "✅ *Cheksiz imkoniyatlar!*\n\n"
            )
            await bot.send_message(GROUP_ID, text, parse_mode="Markdown")
        except Exception as e:
            logging.error(f"❌ Xatolik yuz berdi: {e}")
        await asyncio.sleep(600)  # 10 daqiqa (600 sekund)

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

# 📌 Tugmalar
def generate_price_buttons(service):
    buttons = [[InlineKeyboardButton(text=f"{duration} - {price}", callback_data=callback)] for _, duration, price, callback in prices[service]]
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_services")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("👋 Assalomu alaykum!\n\n📌 Xizmatlarni ko‘rish yoki 👨‍💼 admin bilan bog‘lanish uchun menyudan foydalaning:", reply_markup=main_menu)

@dp.message()
async def handle_message(message: types.Message):
    if message.text == "📌 Xizmatlar":
        await message.answer("📌 *Xizmatlardan birini tanlang:*", reply_markup=services_menu, parse_mode="Markdown")
    elif message.text == "👨‍💼 Admin bilan bog‘lanish":
        admin_button = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👨‍💼 Admin bilan bog‘lanish", url=ADMIN_URL)]
        ])
        await message.answer("👨‍💼 *Admin bilan bog‘lanish uchun tugmani bosing:*", reply_markup=admin_button, parse_mode="Markdown")

@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    if call.data == "premium_service":
        await call.message.edit_text("🚀 *Telegram Premium narxlari:*", reply_markup=generate_price_buttons("premium"), parse_mode="Markdown")
    elif call.data == "stars_service":
        await call.message.edit_text("⭐ *Telegram Stars narxlari:*", reply_markup=generate_price_buttons("stars"), parse_mode="Markdown")
    elif call.data == "uc_service":
        await call.message.edit_text("🎮 *PUBG UC narxlari:*", reply_markup=generate_price_buttons("uc"), parse_mode="Markdown")
    elif call.data == "back_to_main":
        await call.message.edit_text("📌 *Asosiy menyu:*", reply_markup=main_menu, parse_mode="Markdown")
    elif call.data == "back_to_services":
        await call.message.edit_text("📌 *Xizmatlardan birini tanlang:*", reply_markup=services_menu, parse_mode="Markdown")
    elif call.data.startswith("price_"):  
        selected_service, selected_duration, selected_price = price_buttons.get(call.data, ("Noma’lum xizmat", "Noma’lum miqdor", "Noma’lum narx"))
        if "Premium" in selected_service:
            duration_text = f"⏳ *Davomiyligi:* {selected_duration}"
        else:
            duration_text = f"📦 *Miqdori:* {selected_duration}"
        await call.message.edit_text(
            f"✅ *Siz tanlagan xizmat:* {selected_service}\n"
            f"{duration_text}\n"
            f"💰 *Narxi:* {selected_price}\n\n"
            f"💳 *To‘lov uchun karta raqami:* `{ADMIN_CARD_NUMBER}`\n\n"
            "📞 *To‘lov qilganingizdan so‘ng adminga to‘lov chekini yuboring va tasdiqlashini kuting!*",
            parse_mode="Markdown"
        )
    await call.answer()

async def main():
    logging.info("Bot ishga tushdi!")
    asyncio.create_task(send_scheduled_message())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
