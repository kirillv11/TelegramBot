from random import randint
import json
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
import wikipedia
from config import API_TOKEN

# t.me/ExplorationUniverseBot

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    """
    This function will be called when user sends `/start` command
    """
    await message.answer("Здравствуйте! С помощью данного бота вы сможете изучить космос и увидеть уникальные фотографии. Весь список команд можно узнать в меню команд, около ввода сообщения, или ввести команду /help.")


@dp.message_handler(commands=['help'])
async def help_command(message: Message):
    """
    This function return hepl text
    """
    await message.answer("/start - запуск\n/foto - случайное фото\n/fact - случайный факт\n/person - случайный человек, который связан с исследованием вселенной\nзапрос без /, например 'солнце' - вернёт ответ на запрос")


@dp.message_handler(commands=['foto', 'get_foto', 'image'])
async def space_image(message: Message):
    """
    This function retur random space image
    """
    with open('data.json', encoding='utf-8') as file:
        file_content = file.read()
        templates = json.loads(file_content)
        length = len(templates['image'])
        number = randint(0, length - 1)
        with open(templates['image'][number]['path'], "rb") as photo:
            await message.answer_photo(photo, caption=f"""
            <b>{templates['image'][number]['name']}</b>\n\n
            {templates['image'][number]['description']}
            """)

    
@dp.message_handler(commands=['fact', 'get_foto'])
async def space_fact(message: Message):
    """
    This function return random fact about space
    """
    with open('data.json', encoding='utf-8') as file:
        file_content = file.read()
        templates = json.loads(file_content)
        length = len(templates['facts'])
        number = randint(0, length - 1)
        await message.answer(f"{templates['facts'][number]}")


@dp.message_handler(commands=['person'])
async def person(message: Message):
    """
    This function return person Which is associated with space
    """
    with open('data.json', encoding='utf-8') as file:
        file_content = file.read()
        templates = json.loads(file_content)
        length = len(templates['person'])
        number = randint(0, length - 1)
        with open(templates['person'][number]['path_image'], "rb") as photo:
            await message.answer_photo(photo, caption=f"<b>{templates['person'][number]['fullname']}</b>\n\nГоды жизни: {templates['person'][number]['date']}\n\n<a href=\"{templates['person'][number]['url']}\">читать подробнее</a>")


@dp.message_handler()
async def search_wikipedia(message: Message):
    """
    This function return wikipedia article
    """
    wikipedia.set_lang('ru')
    response = wikipedia.page(message.text)
    await message.answer(f"<b>{response.title}</b>\n\n{response.summary}\n\n<a href=\"{response.url}\">читать подробнее</a>")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
