from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram.enums import ContentType
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.api.entities import MediaAttachment
from aiogram import Bot, Dispatcher, Router
from aiogram.types import ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
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


class StartSG(StatesGroup):
    start = State()

# Вариант, где медиа (фото) предается в виджет через путь к файлу
async def media_getter(**kwargs):
    photo = MediaAttachment(type=ContentType.PHOTO, path='widget_examples/cat_it.png')
    return {'photo': photo}


start_dialog = Dialog(
    Window(
        Const(text='А этот кот умеет программировать даже хорошо!'),
        DynamicMedia('photo'),
        getter=media_getter,
        state=StartSG.start,
    ),
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