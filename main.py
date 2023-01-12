from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import API_TOKEN
from random import randint
import json

# t.me/ExplorationUniverseBot

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['foto', 'get_foto'])
async def space_image(message: Message):
    """
    This function return the random space image
    """
    with open('data.json', encoding='utf-8') as file:
        file_content = file.read()
        templates = json.loads(file_content)
        length = len(templates['image'])
        number = randint(0, length - 1)
        with open(templates['image'][number]['path'], "rb") as photo:
            await message.answer_photo(photo, caption=f"<b>{templates['image'][number]['name']}</b>\n\n{templates['image'][number]['description']}")

    
@dp.message_handler(commands=['fact'])
async def space_fact(message: Message): ...


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
