from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду /start
@dp.message(CommandStart())
async def command_start_process(message: Message):
    button_1 = InlineKeyboardButton(
        text='✅ Да',
        callback_data='yes'
    )
    button_2 = InlineKeyboardButton(
        text='✖️ Нет',
        callback_data='no'
    )
    markup = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2]])

    await message.answer(
        text=f'Привет, <b>{message.from_user.username}</b>!\n\n'
             f'Пробовали ли вы уже писать ботов с использованием '
             f'библиотеки <code>aiogram_dialog</code>?',
        reply_markup=markup
    )


# Этот хэндлер будет срабатывать нажатие кнопки с callback_data `yes`
@dp.callback_query(F.data == 'yes')
async def yes_click_process(callback: CallbackQuery):
    await callback.message.edit_text(
        text='<b>Прекрасно!</b>\n\nНадеюсь, вы найдете в этом курсе что-то '
             'новое и полезное для себя!'
    )


# Этот хэндлер будет срабатывать нажатие кнопки с callback_data `no`
@dp.callback_query(F.data == 'no')
async def no_click_process(callback: CallbackQuery):
    await callback.message.edit_text(
        text='<b>Попробуйте!</b>\n\nСкорее всего, вам понравится!'
    )


dp.run_polling(bot)