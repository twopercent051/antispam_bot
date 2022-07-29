from aiogram import types, Dispatcher

import json
import string

async def censor_not(message: types.Message):
    pass
async def censor(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split()}\
        .intersection(set(json.load(open('black_list.json')))) != set():
        text = [
            'Спам и реклама в чате запрещены 🤬',
            'Для согласования обратитесь к администратору'
        ]
        await message.reply('\n'.join(text))
        await message.delete()


def register_other(dp : Dispatcher):
    dp.register_message_handler(censor_not, is_chat_admin=True)
    dp.register_message_handler(censor)




