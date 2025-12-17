import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto
)
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

# =======================
# НАСТРОЙКИ
# =======================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Не задан BOT_TOKEN")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

# =======================
# ФОТО (URL-ЗАГЛУШКИ)
# =======================
PHOTO_Q1 = "https://img.freepik.com/premium-photo/traditional-new-year-celebration-china-happy-smile-fireworks-dance_991182-17112.jpg?semt=ais_items_boosted&w=740"
PHOTO_Q2 = "https://cs2.livemaster.ru/storage/d5/4b/bcfa0d2d43ea743e175ba2847dts--odezhda-para-ded-moroz-i-snegurochka.jpg"
PHOTO_Q3 = "https://img.freepik.com/premium-photo/girl-with-sparkler_1048944-5655681.jpg?semt=ais_hybrid&w=740"
PHOTO_Q4 = "https://th-i.thgim.com/public/incoming/d86bqz/article69056997.ece/alternates/FREE_1200/Getty%20Images.jpg"
PHOTO_Q5 = "https://ussa.su/storage/news/1502.jpg"
PHOTO_Q6 = "https://cdn-image.zvuk.com/pic?type=release&id=35883079&size=large&hash=c11039fe-d029-426b-8322-26e39fe64c77"
PHOTO_Q7 = "https://img.freepik.com/premium-vector/real-life-family-moments-vector-illustration-concepts_1253202-60787.jpg?semt=ais_hybrid&w=740"
PHOTO_Q8 = "https://konstruktortestov.ru/files/5520/931d/f52d/4a59/3352/6efa/79e2/73a9/1995992051.jpg"
PHOTO_Q9 = "https://cdn.culture.ru/images/d442f226-9d98-5edc-a0e0-24b176ec4b5d"
PHOTO_Q10 = "https://www.mos.ru/upload/newsfeed/newsfeed/5D3_3945kopiya.JPG"

PHOTO_RESULT = "https://s13.stc.all.kpcdn.net/family/wp-content/uploads/2023/12/photo-f-y-in-article-novogodnie-otkrytki-loshad-1024x1024-25-18.jpg"

QUESTION_PHOTOS = [
    PHOTO_Q1,
    PHOTO_Q2,
    PHOTO_Q3,
    PHOTO_Q4,
    PHOTO_Q5,
    PHOTO_Q6,
    PHOTO_Q7,
    PHOTO_Q8,
    PHOTO_Q9,
    PHOTO_Q10,
]

# =======================
# ВОПРОСЫ (АДАПТАЦИЯ ПОД ДЕТЕЙ)
# =======================
QUESTIONS = [
    {
        "text": "🎄 В какой стране на Новый год любят шумно веселиться и запускать фейерверки?",
        "answers": [
            ("Китай", "fun"),
            ("Норвегия", "family"),
            ("Швейцария", "calm"),
        ],
    },
    {
        "text": "🎁 Где подарки на Новый год приносят Дед Мороз и Снегурочка?",
        "answers": [
            ("Россия", "family"),
            ("Италия", "fun"),
            ("Япония", "calm"),
        ],
    },
    {
        "text": "🎆 В какой стране Новый год часто встречают прямо на улице?",
        "answers": [
            ("США", "fun"),
            ("Финляндия", "family"),
            ("Австрия", "calm"),
        ],
    },
    {
        "text": "🍇 Где на Новый год загадывают желания и едят виноград?",
        "answers": [
            ("Испания", "fun"),
            ("Швеция", "family"),
            ("Канада", "calm"),
        ],
    },
    {
        "text": "🔔 В какой стране в Новый год звонят в колокола много раз?",
        "answers": [
            ("Япония", "calm"),
            ("Бразилия", "fun"),
            ("Франция", "family"),
        ],
    },
    {
        "text": "🎶 Где принято петь песни и ходить в гости?",
        "answers": [
            ("Англия", "fun"),
            ("Исландия", "calm"),
            ("Польша", "family"),
        ],
    },
    {
        "text": "🎄 Где Новый год — это прежде всего семейный праздник?",
        "answers": [
            ("Россия", "family"),
            ("Австралия", "fun"),
            ("Индия", "calm"),
        ],
    },
    {
        "text": "✨ Где на Новый год любят загадывать желания?",
        "answers": [
            ("Почти везде", "family"),
            ("Только в Европе", "calm"),
            ("Только в Азии", "fun"),
        ],
    },
    {
        "text": "🎊 В какой стране Новый год очень яркий и красочный?",
        "answers": [
            ("Бразилия", "fun"),
            ("Чехия", "calm"),
            ("Литва", "family"),
        ],
    },
    {
        "text": "😊 Какой Новый год тебе больше нравится?",
        "answers": [
            ("Весёлый и шумный", "fun"),
            ("Тёплый и семейный", "family"),
            ("Спокойный и уютный", "calm"),
        ],
    },
]

# =======================
# РЕЗУЛЬТАТЫ
# =======================
RESULTS = {
    "fun": {
        "title": "🎉 Ты любишь весёлый Новый год",
        "text": "Тебе нравятся праздники, игры, смех и яркие эмоции.",
    },
    "family": {
        "title": "🎄 Ты любишь семейный Новый год",
        "text": "Для тебя важно быть рядом с близкими и чувствовать уют.",
    },
    "calm": {
        "title": "✨ Ты любишь спокойный Новый год",
        "text": "Тебе нравится тишина, уют и хорошее настроение.",
    },
}

# =======================
# СОСТОЯНИЕ
# =======================
user_data = {}

# =======================
# КЛАВИАТУРЫ
# =======================
def start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Начать тест", callback_data="start_test")]
        ]
    )

def question_keyboard(index: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=answer[0],
                    callback_data=f"answer:{index}:{answer[1]}"
                )
            ]
            for answer in QUESTIONS[index]["answers"]
        ]
    )

def restart_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔁 Пройти ещё раз", callback_data="start_test")]
        ]
    )

# =======================
# ХЕНДЛЕРЫ
# =======================
@dp.message(CommandStart())
async def start(message: Message):
    text = (
        "👋 Привет!\n\n"
        "Здесь тебя ждёт небольшой новогодний тест.\n"
        "Отвечай на вопросы и узнай, "
        "какой у тебя новогодний стиль 🎄"
    )
    await message.answer(text, reply_markup=start_keyboard())

@dp.callback_query(F.data == "start_test")
async def start_test(call: CallbackQuery):
    user_data[call.from_user.id] = {
        "index": 0,
        "score": {"fun": 0, "family": 0, "calm": 0},
    }

    q = QUESTIONS[0]

    await call.message.answer_photo(
        photo=QUESTION_PHOTOS[0],
        caption=f"<b>{q['text']}</b>",
        reply_markup=question_keyboard(0)
    )
    await call.answer()

@dp.callback_query(F.data.startswith("answer"))
async def process_answer(call: CallbackQuery):
    _, index, category = call.data.split(":")
    index = int(index)

    data = user_data[call.from_user.id]
    data["score"][category] += 1
    data["index"] += 1

    if data["index"] >= len(QUESTIONS):
        await show_result(call)
        return

    next_index = data["index"]
    q = QUESTIONS[next_index]

    await call.message.edit_media(
        media=InputMediaPhoto(
            media=QUESTION_PHOTOS[next_index],
            caption=f"<b>{q['text']}</b>"
        ),
        reply_markup=question_keyboard(next_index)
    )
    await call.answer()

async def show_result(call: CallbackQuery):
    score = user_data[call.from_user.id]["score"]
    result_key = max(score, key=score.get)
    result = RESULTS[result_key]

    text = (
        f"<b>{result['title']}</b>\n\n"
        f"{result['text']}\n\n"
        "🎁 Спасибо за участие!"
    )

    await call.message.edit_media(
        media=InputMediaPhoto(
            media=PHOTO_RESULT,
            caption=text
        ),
        reply_markup=restart_keyboard()
    )
    await call.answer()

# =======================
# ЗАПУСК
# =======================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
