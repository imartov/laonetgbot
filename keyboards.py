from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup)


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
    resize_keyboard=True, # уменьшение размера кнопок
    # one_time_keyboard=True, # сокрытие клавиатуры после первого использования
    input_field_placeholder="Выберете действие из меню", # отображается сообщение
    selective=True # клавиатура активируется у того, кто ее вызвал, если будет False - будет видна у всех пользователей
)

inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подписаться", callback_data="subscribe")
        ]
    ]
)