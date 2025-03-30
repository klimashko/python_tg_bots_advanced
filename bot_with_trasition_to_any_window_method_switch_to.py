from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, Const, Multi, Case, List
from aiogram_dialog.widgets.kbd import Button, Row
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
    window_1 = State()
    window_2 = State()
    window_3 = State()
    window_4 = State()


async def go_first(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=StartSG.window_1)


async def go_second(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=StartSG.window_2)


async def go_third(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=StartSG.window_3)


async def go_fourth(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=StartSG.window_4)


async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    if dialog_manager.start_data:
        getter_data = {'username': event_from_user.username or 'Stranger',
                       'first_show': True}
        dialog_manager.start_data.clear()
    else:
        getter_data = {'first_show': False}
    return getter_data


start_dialog = Dialog(
    Window(
        Format('<b>Привет, {username}!</b>\n', when='first_show'),
        Const('Это <b>первое</b> окно диалога. Выбери в какое окно хочешь перейти 👇'),
        Row(
            Button(Const('2'), id='b_second', on_click=go_second),
            Button(Const('3'), id='b_third', on_click=go_third),
            Button(Const('4'), id='b_fourth', on_click=go_fourth),
        ),
        getter=username_getter,
        state=StartSG.window_1
    ),
    Window(
        Const('Это <b>второе</b> окно диалога. Выбери в какое окно хочешь перейти 👇'),
        Row(
            Button(Const('1'), id='b_first', on_click=go_first),
            Button(Const('3'), id='b_third', on_click=go_third),
            Button(Const('4'), id='b_fourth', on_click=go_fourth),
        ),
        state=StartSG.window_2
    ),
    Window(
        Const('Это <b>третье</b> окно диалога. Выбери в какое окно хочешь перейти 👇'),
        Row(
            Button(Const('1'), id='b_first', on_click=go_first),
            Button(Const('2'), id='b_second', on_click=go_second),
            Button(Const('4'), id='b_fourth', on_click=go_fourth),
        ),
        state=StartSG.window_3
    ),
    Window(
        Const('Это <b>четвертое</b> окно диалога. Выбери в какое окно хочешь перейти 👇'),
        Row(
            Button(Const('1'), id='b_first', on_click=go_first),
            Button(Const('2'), id='b_second', on_click=go_second),
            Button(Const('3'), id='b_third', on_click=go_third),
        ),
        state=StartSG.window_4
    ),
)


@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=StartSG.window_1,
        mode=StartMode.RESET_STACK,
        data={'first_show': True}
    )

if __name__ == '__main__':
    dp.include_router(start_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)