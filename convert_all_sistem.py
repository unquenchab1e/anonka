import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import Message

# ФУНКЦИЯ ПЕРЕВОДА (из 10-й в любую)
def convert_to_base(number, base):
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    if number == 0:
        return "0"

    while number > 0:
        result = digits[number % base] + result
        number = number // base

    return result


# НАСТРОЙКИ БОТА
bot = Bot(token="6307790194:AAEeMIBdDj0QdksNpE1-uxrPUQMaBdh6cZ0")
dp = Dispatcher()

# КОМАНДА /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я перевожу числа между системами счисления.\n\n"
        "Введи три числа через пробел:\n"
        "`<число> <из какой системы> <в какую систему>`\n\n"
        "Например:\n"
        "`255 10 16` → FF\n"
        "`FF 16 10` → 255\n"
        "`11111111 2 10` → 255",
        parse_mode="Markdown")


# ОСНОВНОЙ ОБРАБОТЧИК
@dp.message()
async def convert(message):

    # Разделяем ввод
    part1, base_from, base_to = message.text.split()
    base_from = int(base_from)
    base_to = int(base_to)

    # Переводим число сначала в десятичную
    number_in_decimal = int(part1, base_from)

    # Если целевая система — 10
    if base_to == 10:
        result = str(number_in_decimal)
    else:
        result = convert_to_base(number_in_decimal, base_to)

    await message.answer(f"✨ Результат: {result}")


# ЗАПУСК
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

print('привет привет привет привет')


