from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_add = KeyboardButton('**Добавить**')
button_delete = KeyboardButton('**Удалить**')
button_watch_list = KeyboardButton('**Просмотр чёрного списка**')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_add).add(button_delete).\
    add(button_watch_list)