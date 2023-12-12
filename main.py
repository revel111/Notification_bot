import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, Bot, types

from other_funcs import read_dictionary

bot = Bot(os.environ['TOKEN'])
dp = Dispatcher()
key_words = read_dictionary()


@dp.message()
async def echo_message(message: types.Message):
    user = await bot.get_chat(os.environ['FEEDBACK'])
    user_id = user.id

    for word in key_words:
        if word in message.text:
            await bot.forward_message(chat_id=user_id, message_id=message.message_id,
                                      from_chat_id=message.chat.id)
            break


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


try:
    if __name__ == '__main__':
        asyncio.run(main())
except KeyboardInterrupt as e:
    sys.exit()
