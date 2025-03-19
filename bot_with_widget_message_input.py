from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs, ShowMode
from aiogram_dialog.widgets.text import Format, Const, Multi, Case, List
from aiogram.enums import ContentType, ParseMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const
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


# Хэндлер, который сработает на любой апдейт типа `Message`
# за исключением команды /start
async def message_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager) -> None:
    # dialog_manager.show_mode = ShowMode.NO_UPDATE #с этой строкой не будет отправляться следом за копией сообщение
    # 'Пришлите мне что-нибудь и я отправлю вам копию обратно'
    await message.send_copy(message.chat.id)


start_dialog = Dialog(
    Window(
        Const(text='Пришлите мне что-нибудь и я отправлю вам копию обратно'),
        MessageInput(
            func=message_handler,
            content_types=ContentType.ANY,
        ),
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
