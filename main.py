import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import sql_start, sql_add_words, sql_delete_words, sql_print_words, sql_find_user

bot = Bot(os.environ['TOKEN'])
dp = Dispatcher()

delete_message_keyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[
    [
        InlineKeyboardButton(text='Delete message', callback_data='delete')
    ]
])


class Words(StatesGroup):
    words = State()


@dp.message(CommandStart())
async def echo_on_start(message: types.Message) -> None:
    if message.chat.type == 'private':
        await message.reply(
            'Hello! I am a Telegram bot who help you will notify you if someone typed a word you want to be tracked.\n')
    else:
        await message.reply('This command is only supported in private messages.\n',
                            reply_markup=delete_message_keyboard)


@dp.message(Command('add_words'))
async def echo_add_words(message: types.Message, state: FSMContext) -> None:
    if message.chat.type == 'private':
        await state.set_state(Words.words)
        await message.reply(
            "Type words to be tracked in form of 'word1 word2 word3'.\nType 'cancel' if you want to stop adding "
            "words.\n")
    else:
        await message.reply('This command is only supported in private messages.\n',
                            reply_markup=delete_message_keyboard)


@dp.message(Words.words)
async def fill_words(message: types.Message, state: FSMContext) -> None:
    if message.text == 'cancel':
        await message.reply('Adding words to be tracked was cancelled!\n')
        await state.clear()
        return

    await state.update_data(words=message.text)
    await sql_add_words(message.text.split(), message.from_user.id)
    await message.reply('Words were successfully added!\n')
    await state.clear()


@dp.message(Command('delete_words'))
async def echo_add_words(message: types.Message, ) -> None:
    if message.chat.type == 'private':
        await sql_delete_words(message.from_user.id)
        await message.reply('Words were successfully deleted!\n')
    else:
        await message.reply('This command is only supported in private messages.\n',
                            reply_markup=delete_message_keyboard)


@dp.message(Command('print_words'))
async def echo_add_words(message: types.Message) -> None:
    if message.chat.type == 'private':
        await message.reply(await sql_print_words(message.from_user.id))
    else:
        await message.reply('This command is only supported in private messages.\n',
                            reply_markup=delete_message_keyboard)


@dp.message()
async def forward_message(message: types.Message) -> None:
    if message.chat.type != 'private':
        for user_id in await sql_find_user(message.text.split()):
            await bot.forward_message(chat_id=user_id, message_id=message.message_id, from_chat_id=message.chat.id)


@dp.callback_query()
async def handle_delete(callback: types.CallbackQuery):
    if callback.data == 'delete':
        await callback.message.delete()
        await callback.answer()


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    sql_start()
    await dp.start_polling(bot)


try:
    if __name__ == '__main__':
        asyncio.run(main())
except KeyboardInterrupt as e:
    sys.exit()
