from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подписаться", callback_data="subscribe")
        ]
    ]
)