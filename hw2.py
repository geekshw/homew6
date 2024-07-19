# import logging
# from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton
# from aiogram.utils import executor
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from config import token

# GROUP_CHAT_ID = '-4269502098'

# logging.basicConfig(level=logging.INFO)

# bot = Bot(token=token)
# dp = Dispatcher(bot, storage=MemoryStorage())
# dp.middleware.setup(LoggingMiddleware())

# main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
# main_menu.add(KeyboardButton('О нас'))
# main_menu.add(KeyboardButton('Товары'))
# main_menu.add(KeyboardButton('Заказать'))
# main_menu.add(KeyboardButton('Контакты'))

# contact_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# contact_menu.add(KeyboardButton('Поделиться контактом', request_contact=True))

# products = [
#     {
#         'photo': 'https://icdn.lenta.ru/images/2024/04/04/17/20240404173417768/original_c17b873b545fd9486e2682e211876526.jpg',
#         'description': 'айфон 17',
#         'price': '10000000 руб.',
#         'article': '123456'
#     },
#     {
#         'photo': 'https://wallpapers.com/images/featured/ps5-2va2br9eeb2j1tnl.jpg',
#         'description': 'Ограниченный ps5',
#         'price': '2000000 руб.',
#         'article': '789012'
#     },
# ]

# class OrderForm(StatesGroup):
#     waiting_for_article = State()
#     waiting_for_contact = State()

# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#     await message.answer("Добро пожаловать в Tehno-shop! Выберите нужный раздел:", reply_markup=main_menu)

# @dp.message_handler(Text(equals='О нас'))
# async def about_us(message: types.Message):
#     about_text = "Tehno-shop - лучший магазин смартфонов! Мы предлагаем широкий ассортимент товаров по доступным ценам."
#     await message.answer(about_text)

# @dp.message_handler(Text(equals='Товары'))
# async def list_products(message: types.Message):
#     for product in products:
#         photo = product['photo']
#         description = product['description']
#         price = product['price']
#         article = product['article']
#         caption = f"{description}\nЦена: {price}\nАртикул: {article}"
#         await bot.send_photo(message.chat.id, photo, caption=caption)

# @dp.message_handler(Text(equals='Заказать'))
# async def order_product(message: types.Message):
#     await OrderForm.waiting_for_article.set()
#     await message.answer("Пожалуйста, введите артикул товара, который хотите заказать:")

# @dp.message_handler(state=OrderForm.waiting_for_article)
# async def process_article(message: types.Message, state: FSMContext):
#     article = message.text
#     if any(product['article'] == article for product in products):
#         await state.update_data(article=article)
#         await OrderForm.next()
#         await message.answer("Пожалуйста, поделитесь своим контактом для завершения заказа.", reply_markup=contact_menu)
#     else:
#         await message.answer("Неправильный артикул. Пожалуйста, попробуйте снова.")

# @dp.message_handler(content_types=types.ContentType.CONTACT, state=OrderForm.waiting_for_contact)
# async def process_contact(message: types.Message, state: FSMContext):
#     contact = message.contact
#     user_id = message.from_user.id
#     username = message.from_user.username
#     phone_number = contact.phone_number

#     data = await state.get_data()
#     article = data['article']

#     text = f"Новый заказ:\nАртикул: {article}\nКонтакт: {phone_number}\nПользователь: @{username} (ID: {user_id})"
#     await bot.send_message(GROUP_CHAT_ID, text)
#     await message.answer("Спасибо за заказ! Мы свяжемся с вами в ближайшее время.", reply_markup=main_menu)
#     await state.finish()

# @dp.message_handler(Text(equals='Контакты'))
# async def contacts(message: types.Message):
#     contact_text = "Наши контакты:\nТелефон: +1234567890\nEmail: info@tehno-shop.com\nАдрес: г. Москва, ул. Примерная, д. 1"
#     await message.answer(contact_text)


# executor.start_polling(dp, skip_updates=True)