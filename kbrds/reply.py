'''
This module contains reply buttons
'''

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Получить информацию по товару"),
        ],
        [
            KeyboardButton(text="Остановить уведомления"),
        ],
        [
            KeyboardButton(text="Получить информацию из БД"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберете действие из меню",
    selective=True
)
