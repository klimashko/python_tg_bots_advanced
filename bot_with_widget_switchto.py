from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, Const, Multi, Case, List
from aiogram_dialog.widgets.kbd import Next, Back, Row, SwitchTo
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

start_dialog = Dialog(
    Window(
        Const(
            text='Это <b>первое</b> окно диалога. '

        ),
        Row(
           SwitchTo(Const('2️⃣'), id=('second'),state=StartSG.window_2),
           SwitchTo(Const('3️⃣'), id=('third'), state=StartSG.window_3),
        ),
        state=StartSG.window_1
    ),
    Window(
        Const(
            text='Это <b>второе</b> окно диалога. '

        ),
        Row(
            SwitchTo(Const('1️⃣'), id=('first'), state=StartSG.window_1),
            SwitchTo(Const('3️⃣'), id=('third'), state=StartSG.window_3),
        ),
        state=StartSG.window_2
    ),
    Window(
        Const(
            text='Это <b>третье</b> окно диалога. '

        ),
        Row(
            SwitchTo(Const('1️⃣'), id=('first'), state=StartSG.window_1),
            SwitchTo(Const('2️⃣'), id=('second'), state=StartSG.window_2),
        ),
        state=StartSG.window_3
    ),
)


@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.window_1, mode=StartMode.RESET_STACK, data={'my_data': 'my_data'})


if __name__ == '__main__':
    dp.include_router(start_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)