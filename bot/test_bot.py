import logging
import asyncio
import mysql.connector
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Инициализация хранилища FSM
storage = MemoryStorage()

# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Параметры подключения к базе данных MySQL
DB_CONFIG = {
    'user': 'root',
    'password': 'q1q1q1q1',
    'host': 'localhost',
    'database': 'rasset',
    'raise_on_warnings': True
}

# Инициализация бота и диспетчера
bot = Bot(token="7109502996:AAESF07uLWbIKMEMlmYAfpKVBMbebbcZmHs")
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

# Определение состояний для FSM
class BirthdayForm(StatesGroup):
    enter_birthday = State()
    enter_username = State()
    enter_location = State()

# Команда /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я бот для хранения дней рождения пользователей. "
                        "Используй /help для списка команд.")


# Команда /help
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.reply("Список команд:\n"
                        "/add_birthday - добавить день рождения\n"
                        "/list_birthdays - список дней рождения")


# Команда /add_birthday
@dp.message_handler(commands=['add_birthday'])
async def cmd_add_birthday(message: types.Message):
    await message.reply("Введите свой день рождения в формате ГГГГ-ММ-ДД (например, 1990-01-01):")
    await BirthdayForm.enter_birthday.set()


# Обработка ответа на команду /add_birthday
@dp.message_handler(state=BirthdayForm.enter_birthday)
async def process_birthday(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['birthday'] = message.text
        data['tgid'] = message.from_user.id  # Добавляем ключ 'tgid' с идентификатором пользователя
    await message.reply("Спасибо! Теперь введите ваш никнейм в Telegram:")
    await BirthdayForm.next()


# Обработка никнейма пользователя
@dp.message_handler(state=BirthdayForm.enter_username)
async def process_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await message.reply("Отлично! Введите ваше местоположение:")
    await BirthdayForm.next()


# Обработка местоположения пользователя
@dp.message_handler(state=BirthdayForm.enter_location)
async def process_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = message.text

        # Сохранение данных пользователя в базу данных
        await save_user_data(data['tgid'], data['birthday'], data['username'], data['location'])

    await message.reply("Ваши данные успешно сохранены!")
    await state.finish()


# Команда /list_birthdays
@dp.message_handler(commands=['list_birthdays'])
async def cmd_list_birthdays(message: types.Message):
    birthdays = await get_birthdays()
    if birthdays:
        response = "Дни рождения пользователей:\n"
        for birthday in birthdays:
            response += f"{birthday['tgusername']} - {birthday['birthday']}\n"
    else:
        response = "Список дней рождения пуст."
    await message.reply(response)


# Функция для сохранения данных пользователя в базе данных
async def save_user_data(tgid, birthday, username, location):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "INSERT INTO users (tgid, birthday, tgusername, location) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (tgid, birthday, username, location))

        conn.commit()
    except mysql.connector.Error as err:
        logging.error("Error while saving user data: %s", err)
    finally:
        cursor.close()
        conn.close()


# Функция для получения списка дней рождения пользователей
async def get_birthdays():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT tgusername, birthday FROM users"
        cursor.execute(query)

        return cursor.fetchall()
    except mysql.connector.Error as err:
        logging.error("Error while getting birthdays: %s", err)
        return None
    finally:
        cursor.close()
        conn.close()


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
