import operator
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, Const, Multi, Case, List
from aiogram_dialog.widgets.kbd import Column, Radio
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
async def get_languages(dialog_manager: DialogManager, **kwargs):
    checked = dialog_manager.find('radio_lang').get_checked()
    language = {
        '1': 'en',
        '2': 'ru',
        '3': 'fr'
    }
    chosen_lang = language['2' if not checked else checked]
    lang = {
        'ru': {
            '1': '🇬🇧 Английский',
            '2': '🇷🇺 Русский',
            '3': '🇫🇷 Французский',
            'text': 'Выберите язык'
        },
        'en': {
            '1': '🇬🇧 English',
            '2': '🇷🇺 Russian',
            '3': '🇫🇷 French',
            'text': 'Choose language'
        },
        'fr': {
            '1': '🇬🇧 Anglais',
            '2': '🇷🇺 Russe',
            '3': '🇫🇷 Français',
            'text': 'Choisissez la langue'
        }
    }
    languages = [
        (f"{lang[chosen_lang]['1']}", '1'),
        (f"{lang[chosen_lang]['2']}", '2'),
        (f"{lang[chosen_lang]['3']}", '3'),
    ]
    return {"languages": languages,
            'text': lang[chosen_lang]['text']}


start_dialog = Dialog(
    Window(
        Format(text='{text}'),
        Column(
            Radio(
                checked_text=Format('🔘 {item[0]}'),
                unchecked_text=Format('⚪️ {item[0]}'),
                id='radio_lang',
                item_id_getter=operator.itemgetter(1),
                items="languages",
            ),
        ),
        state=StartSG.start,
        getter=get_languages
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