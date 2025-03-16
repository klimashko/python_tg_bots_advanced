from aiogram import Bot, Dispatcher, Router
from aiogram.types import ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const, Multi, Case, List
from aiogram_dialog.widgets.kbd import Button, Url
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


class StatesSG(StatesGroup):
    start = State()
    newimage = State()



async def button_clicked(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.next()

start_dialog = Dialog(
    Window(
        Const(text='Даже кот умеет программировать!'),
        StaticMedia(
            path='widget_examples/cat_it.png',
            type=ContentType.PHOTO
        ),
        Button(
            text=Const('Нажми'),
            id='button_1',
            on_click=button_clicked
        ),
        state=StatesSG.start,
    ),
    Window(
        Const(text='А это кот умеет программировать даже хорошо!'),
        StaticMedia(
            url='https://telegra.ph/file/ac76e3f1551f7d59de970.jpg',
            type=ContentType.PHOTO
        ),
        state=StatesSG.newimage,
    ),
)


@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    logger.info(
        f"Получена команда: {message.text} от {message.from_user.full_name} (ID: {message.from_user.id})")
    await dialog_manager.start(state=StatesSG.start, mode=StartMode.RESET_STACK)


if __name__ == '__main__':
    dp.include_router(start_dialog)
    dp.include_router(router)
    setup_dialogs(dp)
    dp.run_polling(bot)