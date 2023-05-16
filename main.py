import json
import wikipedia
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from random import choice
from config import API_TOKEN

# Initialize wikipedia language
wikipedia.set_lang('ru')

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


# Load data from JSON file
file = open('data.json', encoding='utf-8')
templates = json.load(file)


# This function is called when user sends '/start' command
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
	"""
	Sends greeting message to the user
	"""
	await message.answer(
		"Здравствуйте! С помощью данного бота вы сможете изучить космос и увидеть уникальные фотографии. Весь список команд можно узнать в меню команд, около ввода сообщения, или ввести команду /help."
		)


# This function returns help text to the user
@dp.message_handler(commands=['help'])
async def help_command(message: Message):
	"""
	Sends list of available commands to the user
	"""
	await message.answer(
		"/start - запуск\n/foto - случайное фото\n/fact - случайный факт\n/person - случайный человек, который связан с исследованием вселенной\nзапрос без /, например 'солнце', - вернёт ответ на запрос"
		)


# This function returns a random space image to the user
@dp.message_handler(commands=['foto', 'get_foto', 'image'])
async def space_image(message: Message):
	"""
	This function return random space image
	"""
	image = choice(templates['image'])
	with open(image['path'], "rb") as photo:
		await message.answer_photo(
			photo,
			caption=f"<b>{image['name']}</b>\n\n{image['description']}"
		)


# This function returns a random fact about space to the user
@dp.message_handler(commands=['fact', 'get_foto'])
async def space_fact(message: Message):
	"""
	This function return random fact about space
	"""
	fact = choice(templates['facts'])
	await message.answer(f"<b>Интересный факт</b>\n\n{fact}")


# This function returns information about a person associated with space exploration to the user
@dp.message_handler(commands=['person'])
async def person(message: Message):
	"""
	This function return person Which is associated with space
	"""
	data_person = choice(templates['person'])
	with open(data_person['path_image'], "rb") as photo:
		await message.answer_photo(
			photo,
			caption=f"<b>{data_person['fullname']}</b>\n\nГоды жизни: {data_person['date']}\n\n<a href=\"{data_person['url']}\">читать подробнее</a>"
		)


# This function searches for a Wikipedia article based on the user's input
@dp.message_handler()
async def search_wikipedia(message: Message):
	"""
	This function return wikipedia article
	"""
	try:
		response = wikipedia.page(message.text)
		await message.answer(
			f"<b>{response.title}</b>\n\n{response.summary}\n\n<a href=\"{response.url}\">читать подробнее</a>"
			)
	except wikipedia.exceptions.PageError:
		await message.answer(f"Ошибка! Страница не найдена.")
	except:
		await message.answer(f"Ошибка! Ответ на запрос '{message.text}' не найден.")


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
	file.close()
