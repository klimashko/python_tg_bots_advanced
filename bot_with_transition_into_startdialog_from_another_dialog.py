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




class StartSG(StatesGroup):
    start = State()


class SecondDialogSG(StatesGroup):
    start = State()


async def go_start(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


async def start_second(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=SecondDialogSG.start)


async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    print(f'dialog_start_data={dialog_manager.start_data}')
    return {'username': event_from_user.username or 'Stranger'}


start_dialog = Dialog(
    Window(
        Format('<b>Привет, {username}!</b>\n'),
        Const('Нажми на кнопку,\nчтобы перейти во второй диалог 👇'),
        Button(Const('Кнопка'), id='go_second', on_click=start_second),
        getter=username_getter,
        state=StartSG.start
    ),
)

second_dialog = Dialog(
    Window(
        Const('Нажми на кнопку,\nчтобы вернуться в стартовый диалог 👇'),
        Button(Const('Кнопка'), id='button_start', on_click=go_start),
        state=SecondDialogSG.start
    ),
)


@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK, data={'my_data': 'my_data'})


if __name__ == '__main__':
    dp.include_router(start_dialog)
    dp.include_router(second_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)