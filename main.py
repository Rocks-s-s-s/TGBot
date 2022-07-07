from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ContentType, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from config import TOKEN

'''
Бот, хранящий записи человека в файле.
При старте появляется 2 кнопки: 
1. Добавить 
2. Показать все записи
После нажатия на кнопку "Добавить", бот предлагает ввести текст.
Данный текст заносится в файл.
При нажатии на кнопку Показать все записи, выводятся все записи, которые есть в базе.
'''
# TODO: 1. Доделать вывод All entries.

print("Platypus-bot")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

isAdd = False

file = open('DB', 'r+')

buttonAdd = KeyboardButton('Add')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

buttonAllEntries = KeyboardButton('All entries')
keyboard.row(buttonAdd, buttonAllEntries)


@dp.message_handler(commands=['start', 'старт', 'cnfhn'])
async def process_start_command(message: types.Message):
    await message.answer(emojize("Что тебе надо сталкер :question:"), reply_markup=keyboard)


@dp.message_handler(chat_type=[types.ChatType.GROUP, types.ChatType.CHANNEL, types.ChatType.PRIVATE])
async def get_message(message: types.Message):
    global isAdd
    if isAdd:
        file.write(message.text)
        file.flush()
        isAdd = False
    if message.text == 'Add':
        isAdd = True
        await message.delete()
        await message.answer('Введите тест')
    if message.text == '':
        await message.answer('')
    if message.text == 'platapus':
        await bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    if message.text == 'расскажи историю':
        await message.answer(
            'Както рас я не в значай сунул хуй в английский чай, в этот мик всё стало клёвым: хуй английским, чай хуёвым.')


# @dp.callback_query_handler(func=lambda b: b.data == 'buttonStart')
# async def buttonStartClick(Colbec):
@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    print('id: ', msg.sticker.file_id)
    await bot.send_message(msg.from_user.id, msg.sticker.file_id)


if __name__ == '__main__':
    executor.start_polling(dp)
