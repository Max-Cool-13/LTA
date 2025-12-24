import asyncio
import os
from collections import defaultdict

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto,
    BotCommand,
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

# -------------------- ENV --------------------
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# -------------------- BOT --------------------
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML"),
)
dp = Dispatcher(storage=MemoryStorage())

# -------------------- FSM --------------------
class TestState(StatesGroup):
    question = State()

# -------------------- RESULTS (8) --------------------
RESULTS = {
    "tree": {
        "photo": "https://i.pinimg.com/originals/23/ae/9c/23ae9c59ed0a347cd53796c0fef9055b.jpg",
        "text": "🎄 <b>Ты — новогодняя ёлка</b>\nТы создаёшь атмосферу и объединяешь людей.",
    },
    "ginger": {
        "photo": "https://i.ytimg.com/vi/KAxoF4dGaqA/maxresdefault.jpg",
        "text": "🍪 <b>Ты — пряничный человечек</b>\nДобрый, уютный и весёлый.",
    },
    "costume": {
        "photo": "https://cs9.pikabu.ru/post_img/2019/11/13/5/og_og_1573625446224520918.jpg",
        "text": "🎭 <b>Ты — новогодний костюм</b>\nЯркий и запоминающийся.",
    },
    "candy": {
        "photo": "https://img.freepik.com/premium-vector/christmas-candy-set_149267-80.jpg?semt=ais_hybrid&w=740",
        "text": "🍭 <b>Ты — леденец</b>\nЭнергичный и позитивный.",
    },
    "snowflake": {
        "photo": "https://tamtravel.ru/wp-content/uploads/2024/01/winter-ice-close-up-blue-frost-backgrounds-snow-generative-ai_188544-9128.jpg",
        "text": "❄️ <b>Ты — снежинка</b>\nСпокойный и особенный.",
    },
    "toy": {
        "photo": "https://img.joomcdn.net/d1960ad56ac3eae20d6cca80adedbf8022c51fc3_original.jpeg",
        "text": "🎁 <b>Ты — ёлочная игрушка</b>\nУкрашаешь любой праздник.",
    },
    "firework": {
        "photo": "https://avatars.mds.yandex.net/i?id=47b57ab9ad9a5bfa654adadc9a3133fc_l-5287068-images-thumbs&n=13",
        "text": "🎆 <b>Ты — фейерверк</b>\nЯркий и взрывной.",
    },
    "gift": {
        "photo": "https://content.img-gorod.ru/pim/products/images/ab/e6/018ed328-7fd1-7ab7-9eb1-31fde479abe6.jpg",
        "text": "📦 <b>Ты — подарок</b>\nПолон сюрпризов.",
    },
}

# -------------------- QUESTIONS (10) --------------------
QUESTIONS = [
    {
        "photo": "https://img.freepik.com/premium-photo/christmas-tree-background_1071931-66229.jpg",
        "text": "Что ты делаешь первым делом перед праздником?",
        "answers": {
            "Украшаю всё вокруг": "tree",
            "Пеку сладости": "ginger",
            "Придумываю образ": "costume",
            "Жду подарки": "gift",
        },
    },
    {
        "photo": "https://img.freepik.com/premium-photo/snowman-with-christmas-tree-presents_409674-14473.jpg",
        "text": "Какой ты в компании?",
        "answers": {
            "Объединяю всех": "tree",
            "Добрый и тёплый": "ginger",
            "Самый заметный": "firework",
            "Весёлый": "candy",
        },
    },
    {
        "photo": "https://img.freepik.com/premium-photo/glowing-holiday-lights-transparent_87720-65524.jpg",
        "text": "Что тебе ближе?",
        "answers": {
            "Традиции": "tree",
            "Уют": "snowflake",
            "Яркость": "firework",
            "Сюрпризы": "gift",
        },
    },
    {
        "photo": "https://vologda-poisk.ru/system/Cover/images/000/048/496/big/novyy-god-rossiyanovyy-god-rossiya.jpg",
        "text": "Какой подарок ты бы выбрал?",
        "answers": {
            "Красивый": "toy",
            "Вкусный": "ginger",
            "Необычный": "costume",
            "Сладкий": "candy",
        },
    },
    {
        "photo": "https://s2.fotokto.ru/photo/full/248/2480900.jpg",
        "text": "Твоя главная черта?",
        "answers": {
            "Надёжность": "tree",
            "Доброта": "ginger",
            "Креатив": "costume",
            "Энергия": "firework",
        },
    },
    {
        "photo": "https://avatars.mds.yandex.net/i?id=2fb7a786af30b69760a6ecd7262e7ae4_l-4571839-images-thumbs&n=13",
        "text": "Как проходит идеальный праздник?",
        "answers": {
            "Все вместе": "tree",
            "Спокойно": "snowflake",
            "Шумно": "firework",
            "Весело": "candy",
        },
    },
    {
        "photo": "https://i.pinimg.com/originals/46/5c/5c/465c5c63b2990909348b5089c3fe84a6.png",
        "text": "Что ты любишь больше?",
        "answers": {
            "Огоньки": "toy",
            "Сладости": "candy",
            "Наряды": "costume",
            "Сюрпризы": "gift",
        },
    },
    {
        "photo": "https://cdn.culture.ru/images/e630fa35-22be-5fc8-9287-0196650bc976",
        "text": "Как ты радуешь других?",
        "answers": {
            "Создаю атмосферу": "tree",
            "Угощаю": "ginger",
            "Удивляю": "firework",
            "Дарю подарки": "gift",
        },
    },
    {
        "photo": "https://otkritkis.com/wp-content/uploads/2021/11/novogodnyaa-elka-dlya-detey-1.jpg",
        "text": "Какой ты на празднике?",
        "answers": {
            "Центр внимания": "firework",
            "Украшение": "toy",
            "Душа компании": "candy",
            "Спокойный": "snowflake",
        },
    },
    {
        "photo": "https://avatars.mds.yandex.net/i?id=94e51d6cf152c25e0a7c556445b395c3_l-8497316-images-thumbs&n=13",
        "text": "Что для тебя Новый год?",
        "answers": {
            "Традиции": "tree",
            "Чудо": "gift",
            "Веселье": "candy",
            "Красота": "toy",
        },
    },
]

# -------------------- KEYBOARDS --------------------
def control_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🚀 Запуск", callback_data="start_test"),
            InlineKeyboardButton(text="🔄 Перезапуск", callback_data="restart"),
        ]]
    )

def answers_keyboard(answers: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=key)]
            for text, key in answers.items()
        ]
    )

# -------------------- HANDLERS --------------------
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    sent = await message.answer_photo(
        photo=QUESTIONS[0]["photo"],
        caption="🎄 <b>Новогодний тест</b>\n\nОтветь на вопросы и узнай,\nкакой ты новогодний символ!",
        reply_markup=control_keyboard(),
    )
    await state.update_data(msg_id=sent.message_id)

@dp.callback_query(F.data == "start_test")
async def start_test(cb: CallbackQuery, state: FSMContext):
    await state.set_state(TestState.question)
    await state.update_data(step=0, scores=defaultdict(int))
    await show_question(cb.message, state)

@dp.callback_query(F.data == "restart")
async def restart(cb: CallbackQuery, state: FSMContext):
    await start_test(cb, state)

@dp.callback_query(TestState.question)
async def answer(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    step = data["step"]
    scores = data["scores"]

    scores[cb.data] += 1
    step += 1

    if step >= len(QUESTIONS):
        result_key = max(scores, key=scores.get)
        result = RESULTS[result_key]

        await bot.edit_message_media(
            chat_id=cb.message.chat.id,
            message_id=cb.message.message_id,
            media=InputMediaPhoto(
                media=result["photo"],
                caption=result["text"],
            ),
            reply_markup=control_keyboard(),
        )
        await state.clear()
        return

    await state.update_data(step=step, scores=scores)
    await show_question(cb.message, state)

async def show_question(message: Message, state: FSMContext):
    data = await state.get_data()
    step = data["step"]
    q = QUESTIONS[step]

    await bot.edit_message_media(
        chat_id=message.chat.id,
        message_id=message.message_id,
        media=InputMediaPhoto(
            media=q["photo"],
            caption=f"<b>{step + 1} / {len(QUESTIONS)}</b>\n\n{q['text']}",
        ),
        reply_markup=answers_keyboard(q["answers"]),
    )

# -------------------- COMMANDS MENU --------------------
async def set_bot_commands():
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="menu", description="Главное меню"),
        BotCommand(command="help", description="Помощь по боту"),
    ])

@dp.message(Command("menu"))
async def menu_cmd(message: Message):
    await start(message, FSMContext)

@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "🎄 Это новогодний тест.\n"
        "Отвечай на вопросы и узнай,\n"
        "какой ты новогодний символ!"
    )

# -------------------- RUN --------------------
async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
