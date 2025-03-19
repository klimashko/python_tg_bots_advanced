from aiogram import Bot, Dispatcher, Router
from typing import Any
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs, ShowMode
from aiogram_dialog.widgets.text import Format, Const, Multi, Case, List
from aiogram.enums import ContentType, ParseMode
from aiogram_dialog.widgets.input import MessageInput, ManagedTextInput, TextInput
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


# Проверка текста на то, что он содержит число от 3 до 120 включительно
def age_check(text: Any) -> str:
    if all(ch.isdigit() for ch in text) and 3 <= int(text) <= 120:
        return text
    raise ValueError


# Хэндлер, который сработает, если пользователь ввел корректный возраст
async def correct_age_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    await message.answer(text=f'Вам {text}')


# Хэндлер, который сработает на ввод некорректного возраста
async def error_age_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректный возраст. Попробуйте еще раз'
    )


# Хэндлер, который сработает, если пользователь отправил вообще не текст
async def no_text(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    print(type(widget))
    await message.answer(text='Вы ввели вообще не текст!')


start_dialog = Dialog(
    Window(
        Const(text='Введите ваш возраст'),
        TextInput(
            id='age_input',
            type_factory=age_check,
            on_success=correct_age_handler,
            on_error=error_age_handler,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
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