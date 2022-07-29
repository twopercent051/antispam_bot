from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hcode

import json

from create_bot import bot
from tgbot.keyboards.reply import button_case_admin
from tgbot.misc.states import FSMAdding, FSMDeleting

ID = None

async def admin_start(message: Message):
    global ID
    ID = message.from_user.id
    text = [
        'Вы вошли как администратор',
        'Пока я умею работать только с одним админом',
        'Для редактирования стоп-листа используйте кнопки ниже'
    ]
    await bot.send_message(message.from_user.id, '\n'.join(text), reply_markup=button_case_admin)
    await message.delete()

async def add_words_start(message: Message):
    if message.from_user.id == ID:
        text = [
            'Введите новые выражения в ЧС, каждое отдельным сообщением',
            'Вводить можно любым регистром (фильтруются все раскладки)'
        ]
        await FSMAdding.adding.set()
        await message.answer('\n'.join(text))

async def add_words(message: Message):
    if message.from_user.id == ID:
        new_word = str(message.text).lower().strip()
        with open('black_list.json', encoding='utf-8') as file:
            black_list = list(json.load(file))
        if new_word not in black_list:
            black_list.append(new_word)
            with open('black_list.json', 'w', encoding='utf-8') as file:
                json.dump(black_list, file, indent=4, ensure_ascii=False)
            text = [
                f'Вы добавили слово {hcode(new_word)}',
                'Добавьте ещё выражение или выберите действие на клавиатуре снизу'
            ]
        else:
            text = [
                'Такое слово уже присутствует в ЧС'
            ]
        await message.answer('\n'.join(text))
async def delete_words_start(message: Message):
    if message.from_user.id == ID:
        text = [
            'В сообщении выше вы получили текущий ЧС',
            'Скопируйте и вставьте те выражения, которые нужно удалить'
        ]
        await FSMDeleting.deleting.set()
        with open('black_list.json', encoding='utf-8') as file:
            black_list = json.load(file)
        await message.answer('\n'.join(black_list))
        await message.answer('\n'.join(text))

async def delete_words(message: Message):
    if message.from_user.id == ID:
        deleting_word = str(message.text).lower().strip()
        with open('black_list.json', encoding='utf-8') as file:
            black_list = list(json.load(file))
        if deleting_word in black_list:
            black_list.remove(deleting_word)
            with open('black_list.json', 'w', encoding='utf-8') as file:
                json.dump(black_list, file, indent=4, ensure_ascii=False)
            text = [
                f'Вы удалили слово {hcode(deleting_word)}',
                'Удалите ещё выражение или выберите действие на клавиатуре снизу'
            ]
        else:
            text = [
                f'Слова {hcode(deleting_word)} нет в списке',
                'Проверьте внимательно'
            ]

        await message.answer('\n'.join(text))

async def show_list(message: Message):
    if message.from_user.id == ID:
        with open('black_list.json', encoding='utf-8') as file:
            black_list = list(json.load(file))
        await message.answer('\n'.join(black_list))

def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["moderator"], is_chat_admin=True)
    dp.register_message_handler(add_words_start, Text(equals='**Добавить**', ignore_case=True), state='*')
    dp.register_message_handler(delete_words_start, Text(equals='**Удалить**', ignore_case=True), state='*')
    dp.register_message_handler(show_list, Text(equals='**Просмотр чёрного списка**', \
                                                         ignore_case=True), state='*')
    dp.register_message_handler(add_words, content_types=['text'], state=FSMAdding.adding)
    dp.register_message_handler(delete_words, content_types=['text'], state=FSMDeleting.deleting)


