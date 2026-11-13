# ============================================================
#  ФАКТОБОТ — финальная версия
#  Файл: bot.py
# ============================================================

import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ============ НАСТРОЙКИ ============
# Токен берём из переменной окружения (задаётся в панели хостинга).
# Если переменной нет — используется заглушка (для локального теста впиши сюда).
BOT_TOKEN = os.getenv("BOT_TOKEN", "9253787353:AAHDLiSSa5TIHDOruciK97Pwu-ltVT4l42A")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# ============ КЛАВИАТУРЫ ============
def main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("👷 Гастарбайтер", callback_data="gastarbaiter"),
        InlineKeyboardButton("🤪 Ебанутая девушка", callback_data="crazy_girl"),
        InlineKeyboardButton("💑 Лучшая пара", callback_data="best_couple"),
    )
    return kb


def back_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("⬅️ Вернуться назад", callback_data="back"))
    return kb


# ============ ТЕКСТЫ ============
WELCOME_TEXT = (
    "👋 Привет! Я — <b>Фактобот</b>.\n\n"
    "Я знаю всё (ну почти) о людях вокруг тебя.\n"
    "Правда, иногда с юмором 😏\n\n"
    "👇 Выбирай кнопку и читай факты:"
)

GASTARBAITER_TEXT = (
    "👷 <b>Борис Воздухов</b> — «гастарбайтер» местного разлива.\n\n"
    "• Обещает — и пропадает 🕳\n"
    "• Слово даёт легко, но забывает так же быстро 🤷\n"
    "• Из категории: «позвоню завтра» — звонит через полгода\n"
    "• Надёжность — 0%. Харизма — 100%. Итог: <b>не надёжен</b> ❌"
)

CRAZY_GIRL_TEXT = (
    "🤪 <b>Ирина</b> — самая бестолковая училка во вселенной.\n\n"
    "• Объясняет урок — сама ничего не понимает 🤯\n"
    "• Домашка есть в журнале, но нет в голове\n"
    "• Вместо оценки — философский взгляд в окно 🪟\n"
    "• Её уроки — это квест «пойми сам» 🎮\n"
    "• Уровень: <b>«а что, так можно было?»</b>"
)

BEST_COUPLE_TEXT = (
    "💑 <b>Светлана и Вадим</b> — лучшая пара на свете!\n\n"
    "• <b>Светлана</b> — самая красивая девушка на планете 🌹✨\n"
    "• <b>Вадим</b> — тот, кто ради неё готов на всё 💪\n"
    "• Вместе — идеальная команда 💞\n"
    "• Целуются, ссорятся, мирятся — и снова счастливы 🥰\n"
    "• Пример для всех пар: <b>любите друг друга!</b> ❤️"
)


# ============ ХЕЛПЕР: УДАЛИТЬ СТАРОЕ + ОТПРАВИТЬ НОВОЕ ============
async def replace_message(
    callback: types.CallbackQuery,
    text: str,
    keyboard: InlineKeyboardMarkup
) -> None:
    try:
        await callback.message.delete()
    except Exception as e:
        logging.warning(f"Не удалось удалить сообщение: {e}")

    try:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    except Exception as e:
        logging.error(f"Не удалось отправить сообщение: {e}")

    await callback.answer()


# ============ ОБРАБОТЧИКИ ============
@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    await message.answer(
        WELCOME_TEXT,
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def on_any_text(message: types.Message):
    await message.answer(
        WELCOME_TEXT,
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


@dp.callback_query_handler(lambda c: c.data == "gastarbaiter")
async def cb_gastarbaiter(callback: types.CallbackQuery):
    await replace_message(callback, GASTARBAITER_TEXT, back_button())


@dp.callback_query_handler(lambda c: c.data == "crazy_girl")
async def cb_crazy_girl(callback: types.CallbackQuery):
    await replace_message(callback, CRAZY_GIRL_TEXT, back_button())


@dp.callback_query_handler(lambda c: c.data == "best_couple")
async def cb_best_couple(callback: types.CallbackQuery):
    await replace_message(callback, BEST_COUPLE_TEXT, back_button())


@dp.callback_query_handler(lambda c: c.data == "back")
async def cb_back(callback: types.CallbackQuery):
    await replace_message(callback, WELCOME_TEXT, main_menu())


# ============ ЗАПУСК ============
if __name__ == "__main__":
    print("🚀 Фактобот запущен!")
    executor.start_polling(dp, skip_updates=True)