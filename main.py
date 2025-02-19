
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const  # Здесь будем импортировать нужные виджеты
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


class StartSG(StatesGroup):
    start = State()


async def some_handler(callback: CallbackQuery, dialog_manager: DialogManager):  # Здесь будут хэндлеры
    pass


async def some_getter(**kwargs):  # Здесь будем создавать нужные геттеры
    pass


# Это стартовый диалог
start_dialog = Dialog(
    Window(
        ...  # Здесь будем добавлять виджеты и геттеры
    ),
)


# Этот классический хэндлер будет срабатывать на команду /start
@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


dp.include_router(start_dialog)
setup_dialogs(dp)
dp.run_polling(bot)