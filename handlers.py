from aiogram import Router, F
from aiogram.types import (
    Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
)
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from states import Registration
from buttons import telefon, start_button, skip_button, no_button
from config import bot, CHANNEL

hand_router = Router()

# ================= START =================

@hand_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ilmkon Schoolga ariza topshirish uchun pastdagi tugmani bosing👇", reply_markup=start_button)


@hand_router.callback_query(F.data == "ariza_topsh")
async def ariza_topsh_cmd(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.answer(
        "<b>👋 Assalomu alaykum!</b>\n\n"
        "🏫 <b>Ilmkon School</b> jamoasiga qo‘shilish uchun ariza topshirish sahifasiga xush kelibsiz.\n\n"
        "✍️ Iltimos, <b>To‘liq ism va familiyangizni</b> kiriting:",
        parse_mode="HTML"
    )
    await state.set_state(Registration.waiting_for_name)


# ================= NAME =================

@hand_router.message(Registration.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip() if message.text else ""

    if len(name) < 5 or not " " in name:
        return await message.answer(
            "❌ Iltimos, ism va familiyangizni to‘liq kiriting.\n"
            "Masalan: <i>Ali Valiyev</i>",
            parse_mode="HTML"
        )

    await state.update_data(full_name=name)

    await message.answer(
        "📸 Endi o‘zingizni <b>rasmingizni yuboring</b> (majburiy):",
        parse_mode="HTML"
    )
    await state.set_state(Registration.waiting_for_photo)


# ================= PHOTO =================

@hand_router.message(Registration.waiting_for_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id

    await state.update_data(photo=photo_id)

    await message.answer(
        "✅ <b>Rasm qabul qilindi!</b>\n\n"
        "📞 Endi telefon raqamingizni yuboring:",
        reply_markup=telefon,
        parse_mode="HTML"
    )
    await state.set_state(Registration.phone_number)


@hand_router.message(Registration.waiting_for_photo)
async def photo_error(message: Message):
    await message.answer(
        "❌ Iltimos, faqat <b>rasm yuboring</b>.",
        parse_mode="HTML"
    )


# ================= PHONE =================

@hand_router.message(Registration.phone_number)
async def phone_cmd(message: Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
    elif message.text and message.text.replace("+", "").isdigit():
        phone = message.text
    else:
        return await message.answer(
            "❌ Noto‘g‘ri raqam!\n"
            "📱 Iltimos, to‘g‘ri telefon kiriting yoki tugmadan foydalaning.",
            parse_mode="HTML"
        )

    await state.update_data(phone_number=phone)

    await message.answer(
        "💼 Hozir qayerda ishlaysiz?\n"
        "<i>(Bo‘lmasa: yo‘q deb yozing)</i>",
        reply_markup=no_button,
        parse_mode="HTML"
    )
    await state.set_state(Registration.work)


# ================= WORK =================

@hand_router.message(Registration.work)
async def work_cmd(message: Message, state: FSMContext):
    if not message.text:
        return await message.answer("❌ Iltimos, matn kiriting.")

    await state.update_data(work=message.text)

    await message.answer(
        "📜 Oldin qayerlarda ishlagansiz?\n"
        "<i>(Bo‘lmasa: yo‘q)</i>",
        reply_markup=no_button,
        parse_mode="HTML"
    )
    await state.set_state(Registration.past_work)


# ================= PAST WORK =================

@hand_router.message(Registration.past_work)
async def past_work_cmd(message: Message, state: FSMContext):
    await state.update_data(past_work=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Pedagogika"), KeyboardButton(text="📊 Hisob-kitob")],
            [KeyboardButton(text="📢 Targ'ibotchi"), KeyboardButton(text="🧩 Boshqa")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🎓 Mutaxassisligingizni tanlang:",
        reply_markup=kb,
        parse_mode="HTML"
    )
    await state.set_state(Registration.specialty)


# ================= SPECIALTY =================

@hand_router.message(Registration.specialty)
async def specialty_cmd(message: Message, state: FSMContext):
    if not message.text:
        return await message.answer("❌ Iltimos, variant tanlang.")

    await state.update_data(specialty=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1 yildan kam"), KeyboardButton(text="1-2 yil")],
            [KeyboardButton(text="3-4 yil"), KeyboardButton(text="5+ yil")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "⏳ Tajribangizni tanlang:",
        reply_markup=kb,
        parse_mode="HTML"
    )
    await state.set_state(Registration.experience)


# ================= EXPERIENCE =================

@hand_router.message(Registration.experience)
async def experience_cmd(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)

    await message.answer(
        "👨‍💼 Rahbarlik tajribangiz bormi?\n"
        "<i>Qisqacha yozing yoki 'yo‘q'</i>",
        reply_markup=no_button,
        parse_mode="HTML"
    )
    await state.set_state(Registration.leadership)


# ================= LEADERSHIP =================

@hand_router.message(Registration.leadership)
async def leadership_cmd(message: Message, state: FSMContext):
    await state.update_data(leadership=message.text)

    await message.answer(
        "💡 Nima uchun siz bu lavozimga munosibsiz?\n"
        "👉 <b>Kamida 3 ta sabab yozing</b>",
        parse_mode="HTML"
    )
    await state.set_state(Registration.reasons)


# ================= REASONS =================

@hand_router.message(Registration.reasons)
async def reasons_cmd(message: Message, state: FSMContext):
    if len(message.text.split()) < 3:
        return await message.answer(
            "❌ Kamida 3 ta sabab yozing.",
            parse_mode="HTML"
        )

    await state.update_data(reasons=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧠 O'zim hal qilaman")],
            [KeyboardButton(text="🤝 Yordam so‘rayman")],
            [KeyboardButton(text="⏳ Kutaman")],
            [KeyboardButton(text="❔ Bilmayman")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "⚙️ Muammoli vaziyatda qanday yo‘l tutasiz?",
        reply_markup=kb,
        parse_mode="HTML"
    )
    await state.set_state(Registration.problem_solving)


# ================= PROBLEM =================

@hand_router.message(Registration.problem_solving)
async def problem_cmd(message: Message, state: FSMContext):
    await state.update_data(problem_solving=message.text)

    await message.answer(
        "🏆 Yutuqlaringiz (sertifikat, diplom):",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )
    await state.set_state(Registration.achievements)


# ================= ACHIEVEMENTS =================

@hand_router.message(Registration.achievements)
async def achievements_cmd(message: Message, state: FSMContext):
    await state.update_data(achievements=message.text)

    await message.answer(
        "🏫 Nima uchun aynan <b>Ilmkon School</b>?",
        parse_mode="HTML"
    )
    await state.set_state(Registration.why_ilmkon)


# ================= WHY =================

@hand_router.message(Registration.why_ilmkon)
async def why_cmd(message: Message, state: FSMContext):
    await state.update_data(why_ilmkon=message.text)

    await message.answer(
        "✍️ Qo‘shimcha fikr yoki savollaringiz (ixtiyoriy):",
        reply_markup=skip_button,
        parse_mode="HTML"
    )
    await state.set_state(Registration.extra_comments)


# ================= FINAL =================

@hand_router.message(Registration.extra_comments)
async def final_step(message: Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)

    data = await state.get_data()

    text = (
        f"<b>📩 Yangi ariza</b>\n\n"
        f"👤 <b>Ism:</b> {data.get('full_name')}\n"
        f"📞 <b>Tel:</b> {data.get('phone_number')}\n"
        f"💼 <b>Ish:</b> {data.get('work')}\n"
        f"📜 <b>Oldingi ish:</b> {data.get('past_work')}\n"
        f"🎓 <b>Mutaxassislik:</b> {data.get('specialty')}\n"
        f"⏳ <b>Tajriba:</b> {data.get('experience')}\n"
        f"👨‍💼 <b>Rahbarlik:</b> {data.get('leadership')}\n"
        f"💡 <b>Sabab:</b> {data.get('reasons')}\n"
        f"⚙️ <b>Muammo:</b> {data.get('problem_solving')}\n"
        f"🏆 <b>Yutuq:</b> {data.get('achievements')}\n"
        f"🏫 <b>Nega Ilmkon:</b> {data.get('why_ilmkon')}\n"
        f"✍️ <b>Qo‘shimcha:</b> {data.get('extra_comments')}\n\n"
        f"🆔 {message.from_user.id}"
    )

    try:
        await bot.send_photo(
            chat_id=CHANNEL,
            photo=data.get("photo"),
            caption=text,
            parse_mode="HTML"
        )
    except:
        await bot.send_message(
            chat_id=CHANNEL,
            text=text,
            parse_mode="HTML"
        )

    await message.answer(
        "✅ <b>Rahmat!</b>\n\n"
        "📨 Arizangiz qabul qilindi.\n"
        "📞 Tez orada siz bilan bog‘lanamiz.",
        reply_markup=start_button,
        parse_mode="HTML"
    )

    await state.clear()