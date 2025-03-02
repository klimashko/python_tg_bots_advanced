import random

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, Const, Multi, Case
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


async def get_name(**kwargs):
    return {'number': random.randint(1, 4)}


start_dialog = Dialog(
    Window(
        Case(
            texts={
                1: Const('Это первый текст'),
                2: Const('Это второй текст'),
                3: Const('Это третий текст'),
                ...: Const('Это текст по умолчанию') #Интересное решение для виджета Case -
                # использование эллипсиса (специальной конструкции python - ...)
                # в качестве ключа для значения по умолчанию, то есть для случая,
                # когда не приходит нужный ключ для Case из геттера.
            },
            selector='number',

        ),
        getter=get_name,
        state=StartSG.start
    )
)


@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    logger.info(
        f"Получена команда: {message.text} от {message.from_user.full_name} (ID: {message.from_user.id})")
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)
    await dialog_manager.done() # добавил команду завершить диалог, тк оставалось состояние state=StartSG.start
    # и поэтому на все update была реакция как на команду /start, скорее всего этого бы не понадобилось,
    # если бы у бота были другие состояния кроме state=StartSG.start



if __name__ == '__main__':
    setup_dialogs(dp)
    dp.include_router(router)
    dp.include_router(start_dialog)
    dp.run_polling(bot)