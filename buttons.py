from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup,
    InlineKeyboardButton, InlineKeyboardMarkup
    )

telefon=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Telefon raqam yuborish", request_contact=True)]
    ],
    resize_keyboard=True,one_time_keyboard=True
)

start_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ariza topshirish", callback_data="ariza_topsh", style='success')]
    ]
)

no_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Yo'q")]
    ], resize_keyboard=True, one_time_keyboard=True
)

skip_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="O'tkazib yuborish")]
    ], resize_keyboard=True, one_time_keyboard=True
)
