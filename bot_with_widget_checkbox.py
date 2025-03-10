from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, Const, Multi, Case, List
from aiogram_dialog.widgets.kbd import Button, Select, Checkbox, ManagedCheckbox
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


# Хэндлер, обрабатывающий нажатие кнопки в виджете `Checkbox`
async def checkbox_clicked(callback: CallbackQuery, checkbox: ManagedCheckbox,
                           dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(is_checked=checkbox.is_checked())


# Геттер
async def getter(dialog_manager: DialogManager, **kwargs):
    checked = dialog_manager.dialog_data.get('is_checked')
    return {'checked': checked,
            'not_checked': not checked}


start_dialog = Dialog(
    Window(
        Const(text='Демонстрация работы виджета <code>Checkbox</code>\n'),
        Const(text='Сейчас дополнительного текста нет', when='not_checked'),
        Const(text='Дополнительный текст есть:\n<b>Это дополнительный текст</b>', when='checked'),
        Checkbox(
            checked_text=Const('[V️] Отключить'),
            unchecked_text=Const('[ ] Включить'),
            id='checkbox',
            default=False,
            on_state_changed=checkbox_clicked,
        ),
        state=StartSG.start,
        getter=getter
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