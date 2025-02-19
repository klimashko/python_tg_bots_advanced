from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, Update
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class StartSG(StatesGroup):
    start = State()


async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    print(kwargs)
    return {'username': event_from_user.username}




start_dialog = Dialog(
    Window(
        Format('Привет, {username}!'),
        getter=username_getter,
        state=StartSG.start
    ),
)


@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


if __name__ == '__main__':
    dp.include_router(start_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)