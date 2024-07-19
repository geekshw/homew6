import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_polling
from config import token
from bs4 import BeautifulSoup
import requests
import logging
import sqlite3

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)

DATABASE = 'news.db'

def init_db():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            news TEXT NOT NULL)''')
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
    finally:
        conn.close()

def parse_news():
    try:
        url = 'https://24.kg/'
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad response status
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.select('.item.article-summary')
        parsed_news = []
        for item in news_items:
            title_element = item.find('div', class_='caption')
            if title_element:
                title = title_element.text.strip()
                parsed_news.append(title)
        return parsed_news
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return []
    except AttributeError as e:
        logging.error(f"Attribute error: {e}")
        return []

def save_news_to_db(news_list):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        for news in news_list:
            cursor.execute("INSERT INTO news (news) VALUES (?)", (news,))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
    finally:
        conn.close()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот, который отправляет последние новости в любое время. Нажмите /news")

@dp.message_handler(commands=['news'])
async def cmd_news(message: types.Message):
    try:
        await message.answer("Сейчас отправим вам новости")
        news_list = parse_news()
        if news_list:
            save_news_to_db(news_list)
            for idx, news in enumerate(news_list, start=1):
                await message.answer(f"{idx}. {news}")
        else:
            await message.answer("К сожалению, не удалось получить новости сейчас. Попробуйте позже.")
    except Exception as e:
        logging.error(f"Error processing /news command: {e}")

async def on_startup(dp):
    init_db()

if __name__ == "__main__":
    start_polling(dp, skip_updates=True, on_startup=on_startup)
