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
    resize_keyboard=True, # уменьшение размера кнопок
    input_field_placeholder="Выберете действие из меню", # отображается сообщение
    selective=True # клавиатура активируется у того, кто ее вызвал, если будет False - будет видна у всех пользователей
)
