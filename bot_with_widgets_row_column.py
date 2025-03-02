from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, Const, Multi, Case, List
from aiogram_dialog.widgets.kbd import Button, Row, Column
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


async def button_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.message.answer(f'была нажата кнопка {button.widget_id}')


start_dialog = Dialog(
    Window(
        Const('На кнопки из этого сообщения можно нажать!'),
        Row(
            Button(
                text=Const('Кнопка 1'),
                id='button_1',
                on_click=button_clicked),
            Button(
                text=Const('Кнопка 2'),
                id='button_2',
                on_click=button_clicked),
            Button(
                text=Const('Кнопка 3'),
                id='button_3',
                on_click=button_clicked),
        ),
        Column(
            Button(
                text=Const('Кнопка 4'),
                id='button_4',
                on_click=button_clicked),
            Button(
                text=Const('Кнопка 5'),
                id='button_5',
                on_click=button_clicked),
            Button(
                text=Const('Кнопка 6'),
                id='button_6',
                on_click=button_clicked),
        ),
        state=StartSG.start,
    )
)


@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    logger.info(
        f"Получена команда: {message.text} от {message.from_user.full_name} (ID: {message.from_user.id})")
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


if __name__ == '__main__':
    dp.include_router(start_dialog)
    dp.include_router(router)
    setup_dialogs(dp)
    dp.run_polling(bot)
