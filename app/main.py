import asyncio
import json
from aiogram import Bot, Dispatcher
from app.core.aggregate_serv import get_data
from app.core.settings import settings
from aiogram.types import Message

from app.utils.bot_validation import validate

TOKEN = settings.TG_TOKEN
dp = Dispatcher()
bot = Bot(TOKEN)


@dp.message()
@validate(bot)
async def main_command(message: Message):
    aggregate_filter = json.loads(message.text)
    response_map = await get_data(aggregate_filter)
    response = json.dumps(response_map)
    await bot.send_message(chat_id=message.chat.id, text=response)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
