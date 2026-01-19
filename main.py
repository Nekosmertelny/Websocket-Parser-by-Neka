import websockets
import asyncio
import json
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
import time
binance_url = "wss://fstream.binance.com/ws/btcusdt@aggTrade"
BOT_TOKEN = "7089879181:AAEwc_siTWtgRSc_W7TW9uHKT0wJ8xrpaIA"
MY_USER_ID = 1905145897 
Last_send_time=0

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def get_start(message: Message):
    await message.answer(text=f"Твой ID: {message.from_user.id}")

async def fetch_binance_trades(url: str):
    print(f"Подключение к Binance...")
    async with websockets.connect(url) as ws:
        async for msg in ws:
            data = json.loads(msg)
            price = data.get('p')
            if time.time()-Last_send_time > 5:
                await send_message_to_tg(msg=f"Новая цена: {price}")
async def main():
    print("Бот запущен...")
    await asyncio.gather(
        fetch_binance_trades(binance_url),
        dp.start_polling(bot)
    )
async def send_message_to_tg(msg: str):
    await bot.send_message(
        chat_id=MY_USER_ID,
        text=msg,
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход...")