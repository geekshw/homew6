import logging
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from config import smtp_sender , smtp_sender_password
from config import token


logging.basicConfig(level=logging.INFO)


SMTP_SERVER = 'githup2010@gmail.com'
SMTP_PORT = 587
GMAIL_ADDRESS = 'alibrobek789@gmail.com'
GMAIL_PASSWORD = 'alialiA3'
bot = Bot(token=token)
dp = Dispatcher(bot)


conn = sqlite3.connect('messages.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        subject TEXT,
        message TEXT
    )
''')
conn.commit()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет я могу помочь тебе отправить сообшение, для начала отпрвь мне свой email")


@dp.message_handler(lambda message: message.text.count('@') == 1)
async def process_email(message: types.Message):
    email = message.text.strip()
    await message.reply("Теперь напиши тему письма")

    cursor.execute("INSERT INTO messages (email) VALUES (?)", (email,))
    conn.commit()


@dp.message_handler(lambda message: not message.text.startswith('/') and '@' not in message.text)
async def process_subject(message: types.Message):
    subject = message.text.strip()
    await message.reply("Отлично теперь отпраь мне сообщение которое хочешб написать")

    cursor.execute("UPDATE messages SET subject = ? WHERE id = (SELECT MAX(id) FROM messages)", (subject,))
    conn.commit()


@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_message(message: types.Message):
    msg_text = message.text.strip()
    cursor.execute("UPDATE messages SET message = ? WHERE id = (SELECT MAX(id) FROM messages)", (msg_text,))
    conn.commit()
    cursor.execute("SELECT email, subject, message FROM messages WHERE id = (SELECT MAX(id) FROM messages)")
    email, subject, msg_text = cursor.fetchone()

    send_email(email, subject, msg_text)
    
    await message.reply("Сообщение успешно отправлено и сохранено.")

def send_email(to_email, subject, message_text):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_text, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        logging.info(f"Email sent to {to_email} successfully")
    except Exception as e:
        logging.error(f"Failed to send email to {to_email}. Error: {str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
