# import logging
# import asyncio
# from aiogram import Bot , Dispatcher , types
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State , StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.types import Message
# from aiogram.filters import Command

# from config import token
# from database import Database

# logging.basicConfig(level=logging.INFO)
# bot = Bot(token=token)
# storage = MemoryStorage
# dp = Dispatcher(bot , storage=storage)
# db = Database('sql.db')
# db.create_table()


# class Form(StatesGroup):
#     username = State()

# @dp.message(Command('start'))
# async def start(message: Message , state: FSMContext):
#     await state.set_state(Form.username)
#     await message.reply("Привет ! Как тебя зовут ?")

# @dp.message(Form.username)
# async def process_username(message:Message , state: FSMContext):
#     username = message.text
#     db.add_user(message.from_user.id , username)
#     await state.clear()
#     await message.reply(f"ПРиятно познокомится , {username}!")

# @dp.message(Command('me'))
# async def me(message:Message):
#     user = db.get_user(message.from_user.id)
#     if user:
#         await message.reply(f"")
#     else:
#         await message.reply(f"")
#         await start(message)

# async def on_startup:

# async def main():
#     dp.startup.register()
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())