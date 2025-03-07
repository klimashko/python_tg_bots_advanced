from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, Const, Multi, Case, List
from aiogram_dialog.widgets.kbd import Button, Select
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

# Это хэндлер, срабатывающий на нажатие кнопки с категорией товаров
async def category_selection(callback: CallbackQuery, widget: Select,
                             dialog_manager: DialogManager, item_id: str):
    print(f'Выбрана категория с id={item_id}')


# Это геттер
async def get_categories(**kwargs):
    categories = [
        ('Техника', 1),
        ('Одежда', 2),
        ('Обувь', 3),
    ]
    return {'categories': categories}

start_dialog = Dialog(
    Window(
        Const(text='Выберите категорию:'),
        Select(
            Format('{item[0]}'),
            id='categ',
            item_id_getter=lambda x: x[1],
            items='categories',
            on_click=category_selection,
        ),
        state=StartSG.start,
        getter=get_categories
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