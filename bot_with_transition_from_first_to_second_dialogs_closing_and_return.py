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
    first = State()
    second = State()
    third = State()


class SecondDialogSG(StatesGroup):
    first = State()
    second = State()


async def close_second_dialog(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager):
    await dialog_manager.done()



async def go_second_dialog(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager):
    await dialog_manager.start(state=SecondDialogSG.first)


async def switch_to_first_one(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=StartSG.first)


async def switch_to_first_two(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=StartSG.second)


async def switch_to_first_three(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=StartSG.third)


async def switch_to_second_one(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=SecondDialogSG.first)


async def switch_to_second_two(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=SecondDialogSG.second)


start_dialog = Dialog(
    Window(
        Const('<b>Вы находитесь в первом окне первого диалога</b>\n'),
        Const('Вы можете переключаться между окнами текущего диалога, '
              'или перейти в новый 👇'),
        Row(
            Button(Const('2️⃣'), id='w_second', on_click=switch_to_first_two),
            Button(Const('3️⃣'), id='w_third', on_click=switch_to_first_three),
        ),
        Button(Const('Во 2-й диалог ▶️'), id='go_second_dialog', on_click=go_second_dialog),
        state=StartSG.first
    ),
    Window(
        Const('<b>Вы находитесь во втором окне первого диалога</b>\n'),
        Const('Вы можете переключаться между окнами текущего диалога, '
              'или перейти в новый 👇'),
        Row(
            Button(Const('1️⃣'), id='w_first', on_click=switch_to_first_one),
            Button(Const('3️⃣'), id='w_third', on_click=switch_to_first_three),
        ),
        Button(Const('Во 2-й диалог ▶️'), id='go_second_dialog', on_click=go_second_dialog),
        state=StartSG.second
    ),
    Window(
        Const('<b>Вы находитесь в третьем окне первого диалога</b>\n'),
        Const('Вы можете переключаться между окнами текущего диалога, '
              'или перейти в новый 👇'),
        Row(
            Button(Const('1️⃣'), id='w_first', on_click=switch_to_first_one),
            Button(Const('2️⃣'), id='w_second', on_click=switch_to_first_two),
        ),
        Button(Const('Во 2-й диалог ▶️'), id='go_second_dialog', on_click=go_second_dialog),
        state=StartSG.third
    ),
)


second_dialog = Dialog(
    Window(
        Const('<b>Вы находитесь в первом окне второго диалога!</b>\n'),
        Const('Нажмите на кнопку Отмена,\nчтобы вернуться в стартовый диалог 👇'),
        Button(Const('2️⃣'), id='w_second', on_click=switch_to_second_two),
        Button(Const('Отмена'), id='button_cancel', on_click=close_second_dialog),
        state=SecondDialogSG.first
    ),
    Window(
        Const('<b>Вы находитесь во втором окне второго диалога!</b>\n'),
        Const('Нажмите на кнопку Отмена,\nчтобы вернуться в стартовый диалог 👇'),
        Button(Const('1️⃣'), id='w_first', on_click=switch_to_second_one),
        Button(Const('Отмена'), id='button_cancel', on_click=close_second_dialog),
        state=SecondDialogSG.second
    ),
)


@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.first, mode=StartMode.RESET_STACK, data={'my_data': 'my_data'})


if __name__ == '__main__':
    dp.include_router(start_dialog)
    dp.include_router(second_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)