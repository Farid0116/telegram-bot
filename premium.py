import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# 🔑 Bot tokeni
TOKEN = "7805301069:AAHMZsHBAl1_li5nQF2g4oExMDplCCKpEy8"

# 🔹 Admin sahifasi va karta raqami
ADMIN_URL = "https://t.me/Darkness_premium"
ADMIN_CARD_NUMBER = "9860 0366 0913 7041"
ADMIN_ID = 734940228

# 🔹 Bot va dispatcher yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 📌 Asosiy menyu (2 ta ustunda chiqarish)
main_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="📌 Xizmatlar"), types.KeyboardButton(text="👨‍💼 Admin bilan bog‘lanish")],
        [types.KeyboardButton(text="✉️ Adminga murojaat xati")]
    ],
    resize_keyboard=True
)

# 📌 Xizmatlar menyusi (1 ustun)
services_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🚀 Telegram Premium", callback_data="premium_service")],
    [InlineKeyboardButton(text="⭐ Telegram Stars", callback_data="stars_service")],
    [InlineKeyboardButton(text="🎮 PUBG UC", callback_data="uc_service")],
    [InlineKeyboardButton(text="⚽ Efootball", callback_data="efootball_service")],  # Yangi qo‘shildi
    [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")]
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
        ("🎮 PUBG UC", "60 UC", "15,000 so‘m", "price_uc_60"),
        ("🎮 PUBG UC", "325 UC", "65,000 so‘m", "price_uc_325"),
        ("🎮 PUBG UC", "660 UC", "125,000 so‘m", "price_uc_660")
    ],
    "efootball": [  # ✅ Yangi xizmat qo‘shildi
        ("⚽ Efootball", "130 coin", "17,000 so‘m", "price_efootball_130"),
        ("⚽ Efootball", "260 coin ", "34,000 so‘m", "price_efootball_260"),
        ("⚽ Efootball", "300 coin", "36,000 so‘m", "price_efootball_300"),
        ("⚽ Efootball", "430 coin", "52,000 so‘m", "price_efootball_430"),
        ("⚽ Efootball", "550 coin ", "62,000 so‘m", "price_efootball_550"),
        ("⚽ Efootball", "600 coin", "72,000 so‘m", "price_efootball_600"),
        ("⚽ Efootball", "750 coin", "81,000 so‘m", "price_efootball_750"),
        ("⚽ Efootball", "850 coin", "97,000 so‘m", "price_efootball_850"),
        ("⚽ Efootball", "900 coin", "105,000 so‘m", "price_efootball_900"),
        ("⚽ Efootball", "1040 coin", "113,000 so‘m", "price_efootball_1040"),
        ("⚽ Efootball", "1100 coin", "124,000 so‘m", "price_efootball_1100"),
        ("⚽ Efootball", "1300 coin", "143,000 so‘m", "price_efootball_1300"),
        ("⚽ Efootball", "1400 coin", "159,000 so‘m", "price_efootball_1400"),
        ("⚽ Efootball", "1590 coin", "171,000 so‘m", "price_efootball_1590"),
        ("⚽ Efootball", "1600 coin", "209,000 so‘m", "price_efootball_1600"),
        ("⚽ Efootball", "2130 coin", "220,000 so‘m", "price_efootball_2130"),
        ("⚽ Efootball", "3250 coin", "325,000 so‘m", "price_efootball_3250"),
        ("⚽ Efootball", "5700 coin", "525,000 so‘m", "price_efootball_5700"),
        ("⚽ Efootball", "12800 coin", "1,157,000 so‘m", "price_efootball_12800"),
    ]
}

# 📌 Narx callback ma’lumotlarini bog‘lash
price_buttons = {callback: (service, duration, price) for category in prices.values() for service, duration, price, callback in category}

# 📌 Narx callback ma’lumotlarini bog‘lash
price_buttons = {callback: (service, duration, price) for category in prices.values() for service, duration, price, callback in category}

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

# 📌 Foydalanuvchilarning xabarlarini qayta ishlash
@dp.message()
async def handle_message(message: types.Message):
    if message.text == "/start":
        await message.answer("👋 Assalomu alaykum!\n\n📌 *Xizmatlar*ni ko‘rish yoki 👨‍💼 *admin bilan bog‘lanish* uchun menyudan foydalaning:", reply_markup=main_menu, parse_mode="Markdown")

    elif message.text == "📌 Xizmatlar":
        await message.answer("📌 *Xizmatlardan birini tanlang:*", reply_markup=services_menu, parse_mode="Markdown")

    elif message.text == "👨‍💼 Admin bilan bog‘lanish":
        await message.answer("👨‍💼 *Admin bilan bog‘lanish uchun tugmani bosing:*", reply_markup=admin_button, parse_mode="Markdown")

# 📌 Inline tugmalar orqali xizmatlarni tanlash
@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    # 📌 Xizmatlarni ko‘rsatish
    if call.data == "premium_service":
        await call.message.edit_text("🚀 *Telegram Premium narxlari:*", reply_markup=generate_price_buttons("premium"), parse_mode="Markdown")

    elif call.data == "stars_service":
        await call.message.edit_text("⭐ *Telegram Stars narxlari:*", reply_markup=generate_price_buttons("stars"), parse_mode="Markdown")

    elif call.data == "uc_service":
        await call.message.edit_text("🎮 *PUBG UC narxlari:*", reply_markup=generate_price_buttons("uc"), parse_mode="Markdown")

    elif call.data == "efootball_service":  # ✅ Yangi qo‘shildi
        await call.message.edit_text("⚽ *Efootball narxlari:*", reply_markup=generate_price_buttons("efootball"), parse_mode="Markdown")
        
    # 📌 Narx tanlanganda to‘lov ma’lumoti chiqadi
elif call.data.startswith("price_"):
    selected_service, selected_duration, selected_price = price_buttons.get(call.data, ("Noma’lum xizmat", "Noma’lum miqdor", "Noma’lum narx"))

    # ✅ Miqdor formati (Premium uchun davomiylik, boshqa xizmatlar uchun faqat raqam)
    if "Premium" in selected_service:
        duration_text = f"⏳ *Davomiyligi:* {selected_duration}"
    else:
        duration_text = f"📦 *Miqdori:* {selected_duration}"  # ❗️ Raqam oldida faqat "📦 Miqdori" chiqadi

    await call.message.edit_text(
        f"✅ *Siz tanlagan xizmat:* {selected_service}\n"
        f"{duration_text}\n"
        f"💰 *Narxi:* {selected_price}\n\n"
        f"💳 *To‘lov uchun karta raqami:* `{ADMIN_CARD_NUMBER}`\n\n"
        "📞 *To‘lov qilganingizdan so‘ng adminga to‘lov chekini yuboring va tasdiqlashini kuting!*",
        reply_markup=back_to_prices_button(call.data.split("_")[1]),
        parse_mode="Markdown"
    )

    # 📌 Xizmat narxlariga qaytish
    elif call.data.startswith("back_to_"):
        service = call.data.split("_")[-1]

        service_titles = {
            "premium": "🚀 *Telegram Premium narxlari:*",
            "stars": "⭐ *Telegram Stars narxlari:*",
            "uc": "🎮 *PUBG UC narxlari:*"
        }

        text = service_titles.get(service, "📌 *Xizmat narxlari:*")

        await call.message.edit_text(
            text,
            reply_markup=generate_price_buttons(service),
            parse_mode="Markdown"
        )

    elif call.data == "services_menu":
        await call.message.edit_text("📌 *Xizmatlardan birini tanlang:*", reply_markup=services_menu, parse_mode="Markdown")

    await call.answer()

# 📌 Botni ishga tushirish
async def main():
    logging.info("Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
