from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, Const, Multi, Case, List
from aiogram_dialog.widgets.kbd import Button
from aiogram import F
from aiogram.enums import ParseMode
from environs import Env
import logging

logging.basicConfig(level=logging.INFO)  # Уровень логирования
logger = logging.getLogger(__name__)  # Создаем логгер

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

router = Router()


class StartSG(StatesGroup):
    start = State()


# Это хэндлер, обрабатывающий нажатие инлайн-кнопок
async def button_clicked(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    another_button = dialog_manager.dialog_data.get('another_button')
    dialog_manager.dialog_data.update(another_button=not another_button)


# Это геттер
async def get_button_status(dialog_manager: DialogManager, **kwargs):
    another_button = dialog_manager.dialog_data.get('another_button')
    return {'button_status': another_button}


start_dialog = Dialog(
    Window(
        Const('На кнопки из этого сообщения можно нажать!'),
        Button(
            text=Const('Нажми меня!'),
            id='button_1',
            on_click=button_clicked),
        Button(
            text=Const('И меня нажми!'),
            id='button_2',
            on_click=button_clicked,
            when='button_status'),
        state=StartSG.start,
        getter=get_button_status,
    ),
)


# Это классический хэндлер на команду /start
@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


if __name__ == '__main__':
    dp.include_router(start_dialog)
    dp.include_router(router)
    setup_dialogs(dp)
    dp.run_polling(bot)