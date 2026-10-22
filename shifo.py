import asyncio
import logging
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Railway'da dotenv kerak emas

from aiogram import Bot, Dispatcher, F
# ... qolgan importlar

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! Railway Variables ga qo'shing yoki .env faylni tekshiring.")import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# .env fayldan tokenni yuklash
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# ==================== KLAVIATURALAR ====================
def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🩺 Kasalliklar haqida")],
            [KeyboardButton(text="💊 Dorilar haqida")],
            [KeyboardButton(text="🥗 Sog'lom ovqatlanish")],
            [KeyboardButton(text="📞 Shifokor bilan bog'lanish")],
            [KeyboardButton(text="ℹ️ Bot haqida")],
        ],
        resize_keyboard=True
    )
    return keyboard


def back_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ Orqaga")]],
        resize_keyboard=True
    )
    return keyboard


# ==================== STATES ====================
class Form(StatesGroup):
    kasallik = State()
    dori = State()
    bog = State()


# ==================== START ====================
@dp.message(CommandStart())
async def start_handler(message: Message):
    text = (
        f"Assalomu alaykum, <b>{message.from_user.full_name}</b>! 👋\n\n"
        f"🏥 <b>SHIFO.UZ</b> botiga xush kelibsiz!\n\n"
        f"Bu bot orqali siz:\n"
        f"✅ Kasalliklar haqida ma'lumot olasiz\n"
        f"✅ Dorilar haqida bilib olasiz\n"
        f"✅ Sog'lom ovqatlanish bo'yicha maslahatlar olasiz\n"
        f"✅ Shifokor bilan bog'lanishingiz mumkin\n\n"
        f"⚠️ <i>Diqqat! Botdagi ma'lumotlar faqat ma'lumot uchun. "
        f"Aniq tashxis va davolanish uchun shifokorga murojaat qiling!</i>\n\n"
        f"Kerakli bo'limni tanlang 👇"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu())


# ==================== KASALLIKLAR ====================
@dp.message(F.text == "🩺 Kasalliklar haqida")
async def kasallik_handler(message: Message, state: FSMContext):
    await state.set_state(Form.kasallik)
    await message.answer(
        "🩺 <b>Kasallik nomini yozing:</b>\n\n"
        "Masalan: <i>gripp, bosh og'rig'i, angina, allergiya...</i>",
        parse_mode="HTML",
        reply_markup=back_menu()
    )


@dp.message(Form.kasallik)
async def kasallik_javob(message: Message, state: FSMContext):
    if message.text == "⬅️ Orqaga":
        await state.clear()
        await message.answer("Asosiy menyu:", reply_markup=main_menu())
        return

    kasallik = message.text.lower().strip()

    # Kasalliklar bazasi (o'zingiz kengaytirishingiz mumkin)
    baza = {
        "gripp": (
            "🤒 <b>Gripp</b>\n\n"
            "📌 <b>Belgilari:</b> isitma, bosh og'rig'i, tomoq og'rig'i, "
            "burun oqishi, holsizlik.\n\n"
            "💊 <b>Davolash:</b> ko'p suyuqlik ichish, dam olish, "
            "shifokor tavsiyasi bilan antiviral dorilar.\n\n"
            "⚠️ 3 kundan ortiq isitma bo'lsa, shifokorga murojaat qiling!"
        ),
        "bosh og'rig'i": (
            "🤕 <b>Bosh og'rig'i</b>\n\n"
            "📌 <b>Sabablari:</b> stress, charchoq, uyqu yetishmasligi, "
            "qon bosimi.\n\n"
            "💊 <b>Tavsiya:</b> tinch joyda dam olish, suv ichish, "
            "yengil og'riq qoldiruvchi (shifokor maslahati bilan).\n\n"
            "⚠️ Tez-tez ta"
            "krorlansa, nevrologga murojaat qiling."
        ),
        "angina": (
            "😷 <b>Angina</b>\n\n"
            "📌 <b>Belgilari:</b> tomoq og'rig'i, yutishda qiyinchilik, "
            "isitma, bodomsimon bezlar yallig'lanishi.\n\n"
            "💊 <b>Davolash:</b> shifokor nazorati ostida antibiotiklar, "
            "iliq suyuqlik, yotoq rejimi.\n\n"
            "⚠️ O'z-o'zini davolash xavfli!"
        ),
        "allergiya": (
            "🤧 <b>Allergiya</b>\n\n"
            "📌 <b>Belgilari:</b> teri qichishi, toshma, hapşırık, "
            "ko'z yosh oqishi.\n\n"
            "💊 <b>Tavsiya:</b> allergenni aniqlash, antigistamin dorilar "
            "(shifokor tavsiyasi bilan).\n\n"
            "⚠️ Nafas olish qiyinlashsa, zudlik bilan tez yordam chaqiring!"
        ),
    }

    javob = baza.get(kasallik,
                     f"❌ <b>{message.text}</b> haqida ma'lumot topilmadi.\n\n"
                     f"Boshqa kasallik nomini yozib ko'ring yoki "
                     f"shifokorga murojaat qiling."
                     )

    await message.answer(javob, parse_mode="HTML", reply_markup=back_menu())


# ==================== DORILAR ====================
@dp.message(F.text == "💊 Dorilar haqida")
async def dori_handler(message: Message, state: FSMContext):
    await state.set_state(Form.dori)
    await message.answer(
        "💊 <b>Dori nomini yozing:</b>\n\n"
        "Masalan: <i>paracetamol, aspirin, analgin...</i>",
        parse_mode="HTML",
        reply_markup=back_menu()
    )


@dp.message(Form.dori)
async def dori_javob(message: Message, state: FSMContext):
    if message.text == "⬅️ Orqaga":
        await state.clear()
        await message.answer("Asosiy menyu:", reply_markup=main_menu())
        return

    dori = message.text.lower().strip()

    dorilar = {
        "paracetamol": (
            "💊 <b>Paracetamol</b>\n\n"
            "📌 <b>Qo'llanilishi:</b> isitma, og'riq qoldiruvchi\n"
            "💉 <b>Dozasi:</b> kattalar uchun 500mg, kuniga 3-4 mahal\n"
            "⚠️ <b>Ehtiyot:</b> jigar kasalliklarida ehtiyotkorlik bilan\n"
            "🚫 Spirtli ichimliklar bilan birga ichmang!"
        ),
        "aspirin": (
            "💊 <b>Aspirin</b>\n\n"
            "📌 <b>Qo'llanilishi:</b> og'riq, yallig'lanish, qon suyultirish\n"
            "💉 <b>Dozasi:</b> shifokor tavsiyasi bilan\n"
            "⚠️ <b>Ehtiyot:</b> oshqozon yarasi bo'lsa ichmang\n"
            "🚫 12 yoshgacha bolalarga berilmaydi!"
        ),
        "analgin": (
            "💊 <b>Analgin</b>\n\n"
            "📌 <b>Qo'llanilishi:</b> kuchli og'riq, isitma\n"
            "💉 <b>Dozasi:</b> shifokor tavsiyasi bilan\n"
            "⚠️ <b>Ehtiyot:</b> qonda o'zgarishlar bo'lishi mumkin\n"
            "🚫 Uzoq muddat ishlatilmaydi!"
        ),
    }

    javob = dorilar.get(dori,
                        f"❌ <b>{message.text}</b> haqida ma'lumot topilmadi.\n\n"
                        f"Boshqa dori nomini yozing yoki shifokorga murojaat qiling.\n\n"
                        f"⚠️ <i>Dori ichishdan oldin albatta shifokor bilan maslahatlashing!</i>"
                        )

    await message.answer(javob, parse_mode="HTML", reply_markup=back_menu())


# ==================== OVQATLANISH ====================
@dp.message(F.text == "🥗 Sog'lom ovqatlanish")
async def ovqat_handler(message: Message):
    text = (
        "🥗 <b>Sog'lom ovqatlanish qoidalari</b>\n\n"
        "1️⃣ <b>Nonushta</b> - eng muhim ovqat. Don mahsulotlari, tuxum, sut.\n\n"
        "2️⃣ <b>Kuniga 2-2.5 litr suv</b> iching\n\n"
        "3️⃣ <b>Meva-sabzavotlar</b> - kuniga kamida 400-500g\n\n"
        "4️⃣ <b>Fast food</b> va gazlangan ichimliklardan voz keching\n\n"
        "5️⃣ <b>Shakar va tuz</b> miqdorini kamaytiring\n\n"
        "6️⃣ <b>Ovqatlanish tartibi:</b> kuniga 3-4 mahal, kichik porsiyalarda\n\n"
        "7️⃣ <b>Kechki ovqat</b> yotishdan 3 soat oldin\n\n"
        "8️⃣ <b>Jismoniy faollik</b> - kuniga 30 daqiqa sayr\n\n"
        "💚 Sog'lom bo'ling!"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu())


# ==================== BOG'LANISH ====================
@dp.message(F.text == "📞 Shifokor bilan bog'lanish")
async def bog_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Telegram", url="https://t.me/your_doctor")],
        [InlineKeyboardButton(text="📞 Telefon", url="tel:+998901234567")],
        [InlineKeyboardButton(text="🌐 Veb-sayt", url="https://shifo.uz")],
    ])
    await message.answer(
        "📞 <b>Shifokor bilan bog'lanish</b>\n\n"
        "Quyidagi kanallar orqali bog'lanishingiz mumkin:",
        parse_mode="HTML",
        reply_markup=keyboard
    )


# ==================== BOT HAQIDA ====================
@dp.message(F.text == "ℹ️ Bot haqida")
async def about_handler(message: Message):
    text = (
        "ℹ️ <b>SHIFO.UZ boti haqida</b>\n\n"
        "🤖 <b>Versiya:</b> 1.0\n"
        "👨‍💻 <b>Maqsad:</b> Sog'liq haqida foydali ma'lumot berish\n"
        "📅 <b>Yaratilgan:</b> 2026\n\n"
        "⚠️ <b>Muhim ogohlantirish:</b>\n"
        "Botdagi barcha ma'lumotlar faqat <b>ma'lumot uchun</b>. "
        "Hech qanday tashxis qo'yilmaydi va dori tavsiya etilmaydi. "
        "Aniq tashxis va davolanish uchun <b>shifokorga murojaat qiling</b>!\n\n"
        "💚 <b>SHIFO.UZ</b> - sog'ligingiz bizning g'amxo'rligimizda!"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu())


# ==================== ORQAGA ====================
@dp.message(F.text == "⬅️ Orqaga")
async def back_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Asosiy menyu:", reply_markup=main_menu())


# ==================== BOSHQA XABARLAR ====================
@dp.message()
async def echo_handler(message: Message):
    await message.answer(
        "Iltimos, menyudan kerakli bo'limni tanlang 👇",
        reply_markup=main_menu()
    )


# ==================== ISHGA TUSHIRISH ====================
async def main():
    print("🚀 SHIFO.UZ bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot to'xtatildi")
