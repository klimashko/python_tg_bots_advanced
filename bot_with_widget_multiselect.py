from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
import operator
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Column, Multiselect, Button
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


# Геттер
async def get_topics(dialog_manager: DialogManager, **kwargs):
    topics = [
        ("IT", '1'),
        ("Дизайн", '2'),
        ("Наука", '3'),
        ("Общество", '4'),
        ("Культура", '5'),
        ("Искусство", '6'),
    ]
    return {"topics": topics}


# Обработчик нажатия кнопки "Готово"
async def on_done_pressed(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    selected = dialog_manager.find("multi_topics").get_checked()  # Получаем список выбранных ID
    await callback.message.answer(f"Вы выбрали: {', '.join(selected) if selected else 'ничего'}")
    await dialog_manager.done()  # Закрываем диалог


start_dialog = Dialog(
    Window(
        Const(text='Отметьте темы новостей 👇'),
        Column(
            Multiselect(
                checked_text=Format('[✔️] {item[0]}'),
                unchecked_text=Format('[  ] {item[0]}'),
                id='multi_topics',
                item_id_getter=operator.itemgetter(1),
                items="topics",
            ),
        ),
        Button(Const("✅ Готово"), id="done_btn", on_click=on_done_pressed),
        state=StartSG.start,
        getter=get_topics
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

