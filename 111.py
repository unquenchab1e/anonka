import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart

BOT_TOKEN = "7577204554:AAGKz9jMLMFpbu8djT1GZjzTgqHp6S_WNNQ"
YOUR_TELEGRAM_ID = 631216136

bot = Bot(
    token='7577204554:AAGKz9jMLMFpbu8djT1GZjzTgqHp6S_WNNQ',
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# user_id → ожидает ли ответ
reply_wait = {}  # {admin_id: target_user_id}

@dp.message(CommandStart())
async def handle_start(message: Message):
    await message.answer("Привет! Ты можешь отправить мне своё сообщение *анонимно*. Просто напиши его в чат 👇")

@dp.message(F.text)
async def handle_user_message(message: Message):
    user = message.from_user

    # ✅ Ты отвечаешь через кнопку
    if user.id == 631216136:
        if reply_wait.get(user.id):
            target_user_id = reply_wait.pop(user.id)
            try:
                answer_text = f"📬 *Пришёл ответ:*\n\n{message.text}"
                sent = await bot.send_message(chat_id=target_user_id, text=answer_text, parse_mode="Markdown")
                await message.answer(f"✅ Ответ отправлен (ID: `{sent.message_id}`)", parse_mode="Markdown")
            except Exception as e:
                await message.answer(f"❌ Не удалось доставить сообщение:\n`{str(e)}`", parse_mode="Markdown")
        else:
            await message.answer("❌ Нет активного диалога. Нажми кнопку 'Ответить' под сообщением.")
        return

    # ✅ Получено анонимное сообщение от пользователя
    text = message.text
    user_info = f"""
📩 *Новое сообщение*:

{text}

👤 *Отправитель:*
- username: @{user.username or "не указан"}
- name: {user.first_name} {user.last_name or ""}
- id: {user.id}
""".strip()

    reply_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Ответить", callback_data=f"reply_{user.id}")]
        ]
    )

    await bot.send_message(
        chat_id=631216136,
        text=user_info,
        reply_markup=reply_button
    )

    await message.answer("Сообщение отправлено ✅")

@dp.callback_query(F.data.startswith("reply_"))
async def handle_reply_callback(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    reply_wait[callback.from_user.id] = user_id

    await callback.message.answer("✍️ Введи текст ответа для пользователя.")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())