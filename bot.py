import asyncio
import requests
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from keyboards import kb_start, kb_ml
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

bot = Bot(BOT_TOKEN)

class ML_START(StatesGroup):
    Harry = State()


def get_start_text(name):
    START_TEXT = f"""
    Hello, <b>{name}</b>!
    Choose one of this books and let's start. 
    """
    return START_TEXT


Storage = MemoryStorage()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=Storage)

@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=get_start_text(message.from_user.full_name),
                           parse_mode='HTML',
                           reply_markup=kb_start)



    # await state.finish()

@dp.message_handler(text=['Harry Potter'], state = '*')
async def start_dialog(message: types.Message):
    await bot.send_message(chat_id = message.from_user.id,
                           text = 'Now you cat ask bot any question about this book, for leaving use <b>cancel</b>',
                           parse_mode='HTML',
                           reply_markup=kb_ml)
    await ML_START.Harry.set()

@dp.message_handler(commands=['cancel'], state = '*')
async def start_dialog(message: types.Message, state:FSMContext):
    await bot.send_message(chat_id = message.from_user.id,
                           text = 'Welcome to menu',
                           parse_mode='HTML',
                           reply_markup=kb_start)
    await state.finish()

@dp.message_handler(state=ML_START.Harry)
async def harry_test_api(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=requests.get(f"http://127.0.0.1:8000/predict?question={message.text}").json()[
                               'answer'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    # question = 'Is Malfoy an ally of Voldemort?'
    # text = requests.get(f"http://127.0.0.1:8000/predict?question={question}").json()['answer']
    # print(text)

