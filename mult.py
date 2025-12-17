import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Вопросы теста и возможные ответы
questions = [
    {
        "question": "Какие животные тебе нравятся больше?",
        "options": ["Коты", "Собаки", "Попугаи", "Обезьяны"],
        "image": "https://zamanilka.ru/wp-content/uploads/2022/12/domashnie-zhivotnye-kollazh.png"
    },
    {
        "question": "Какой тип анимации вам больше нравится?",
        "options": ["Рисованная анимация", "Компьютерная графика", "Стоп-моушен анимация", "Смешанная техника"],
        "image": "https://vzlet.org/sites/vzlet.org/files/2019-07/3.6_4.jpg"
    },
    {
        "question": "Какой тон мультфильма вам больше подходит?",
        "options": ["Веселый и легкий", "Темный и мрачный", "Эпический и захватывающий", "Трогательный и душевный"],
        "image": "https://freelance.ru/img/portfolio/pics/00/3B/E8/3926238.jpg"
    },
    {
        "question": "Какой тип героев вам интересен?",
        "options": ["Животные", "Люди", "Роботы или инопланетяне", "Фантастические существа"],
        "image": "https://zabavnikplus.ru/wp-content/uploads/2/b/e/2bebe9f918e583b7e48534c7723b4eda.jpeg"
    },
    {
        "question": "Какую продолжительность мультфильма вы бы выбрали?",
        "options": ["Менее 30 минут", "От 30 до 60 минут", "От 60 до 90 минут", "Более 90 минут"],
        "image": "https://melochovka.ru/wa-data/public/shop/products/88/77/17788/images/13588/13588.750x0.jpg"
    },
    {
        "question": "Какую тематику мультфильма вы бы выбрали?",
        "options": ["Сказки и волшебство", "Научная фантастика", "Исторические сюжеты", "Повседневная жизнь"],
        "image": "https://img.razrisyika.ru/kart/63/1200/249160-geroi-multfilmov-dlya-detey-6-7-let-38.jpg"
    },
    {
        "question": "Какой период создания мультфильма вас больше интересует?",
        "options": ["Классические (до 1980 года)", "Ретро (1980-2000)", "Современные (2000-2015)", "Новинки (после 2015 года)"],
        "image": "https://ic.pics.livejournal.com/luarvik_1221/76592707/74891/74891_900.jpg"
    },
    {
        "question": "Какой формат мультфильма вы предпочитаете?",
        "options": ["Полнометражный фильм", "Короткометражка", "Сериал", "Мюзикл"],
        "image": "https://i.pinimg.com/originals/9a/68/a3/9a68a3198900059b6f226bb0715418b5.jpg"
    },
    {
        "question": "Какой жанр мультфильма вам нравится больше всего?",
        "options": ["Комедия", "Фантастика", "Приключения", "Драма"],
        "image": "https://sun9-17.userapi.com/impg/RdKpzWZwsXaA6xUyiR9wUTRENvouHQpPCukfEA/Qx2EuBhiOzw.jpg?size=604x340&quality=96&sign=58fd7fdc59ea4100372b5bbdf2f37a13&type=album"
    },
    {
        "question": "Какой саундтрек вы бы предпочли в мультфильме?",
        "options": ["Оригинальные песни", "Инструментальная музыка", "Популярные хиты", "Классическая музыка"],
        "image": "https://klike.net/uploads/posts/2023-02/1675320314_3-34.png"
    }
]

# Возможные результаты теста
results = {
    "Остров сокровищ": "https://sneg.top/uploads/posts/2023-03/1680030172_sneg-top-p-oboi-na-telefon-ostrov-sokrovishch-vkontak-1.jpg",
    "Паровозик из Ромашково": "https://images.justwatch.com/poster/178454875/s718/parovozik-iz-romashkova.jpg",
    "Летучий корабль": "https://pushinka.top/uploads/posts/2023-08/1692694143_pushinka-top-p-letuchii-korabl-kartinki-instagram-4.jpg",
    "Ёжик в тумане": "https://bronk.club/uploads/posts/2023-02/1676590434_bronk-club-p-yezhik-v-tumane-otkritka-vkontakte-22.jpg",
    "Как львенок и черепаха пели песню": "https://avatars.dzeninfra.ru/get-zen_doc/1872852/pub_5ec8ba690d590b68ff570870_5ec8bb478ab85d61ea09ea6c/scale_1200",
    "Котёнок по имени Гав": "https://www.timeout.ru/wp-content/uploads/kpposters/392206.jpg",
    "Тайна третьей планеты": "https://cdn.culture.ru/images/d9bb8d62-3633-5490-9bcb-f6b9885ca418",
    "Вовка в тридевятом царстве": "https://i.ytimg.com/vi/JDD0eE_Vy3I/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGH8gNigTMA8=&rs=AOn4CLBqVJnRvxQiWx4--rCTHo6IwXlclg",
    "Малыш и Карлсон": "https://literoved.ru/wp-content/uploads/2021/10/maxresdefault-2.jpg",
    "Жил-был Пес": "https://pic.uma.media/pic/cardimage/5e/cf/5ecfc7abf12e8800c244164d61b3cec9.jpg",
    "Возвращение блудного попугая": "https://gorodprima.ru/wp-content/uploads/2023/06/633d5ea16b570707795d4345dac8bc05-1.jpeg",
    "Смешарики": "https://klike.net/uploads/posts/2022-08/1661857442_j-14.jpg",
    "Золотая антилопа": "https://ucare.timepad.ru/8e5183e3-5f68-4c32-a762-82aebf0e5011/poster_event_2734884.jpg",
}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()  # Сброс данных пользователя
    keyboard = [
        [InlineKeyboardButton("Начать тест", callback_data='start_test')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Готов узнать, какой мульт тебе подойдёт? Жми "Начать тест"!', reply_markup=reply_markup)

# Начало теста
async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['answers'] = []  # Сброс данных пользователя
    await ask_question(update, context, 0)

# Задаем вопрос
async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question_index: int) -> None:
    question = questions[question_index]
    keyboard = [
        [InlineKeyboardButton(option, callback_data=f'answer_{question_index}_{i}')] for i, option in enumerate(question['options'])
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query

    if 'message_id' not in context.user_data:
        message = await query.message.reply_photo(photo=question['image'], caption=question['question'], reply_markup=reply_markup)
        context.user_data['message_id'] = message.message_id
    else:
        media = InputMediaPhoto(media=question['image'], caption=question['question'])
        await query.message.edit_media(media)
        await query.message.edit_reply_markup(reply_markup)

# Обработка ответа
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data.split('_')
    question_index = int(data[1])
    answer_index = int(data[2])
    context.user_data['answers'].append(questions[question_index]['options'][answer_index])
    if question_index + 1 < len(questions):
        await ask_question(update, context, question_index + 1)
    else:
        await show_result(update, context)

# Показ результата
async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = random.choice(list(results.keys()))  # Рандомный выбор результата
    query = update.callback_query
    media = InputMediaPhoto(media=results[result], caption=f"Тест окончен! Тебе подходит: {result}")
    await query.message.edit_media(media)
    await query.message.edit_reply_markup(reply_markup=None)

def main() -> None:
    # Создаем Application и передаем ему токен вашего бота
    application = Application.builder().token("6991573582:AAET5ZxCVw7tkrZKZYIh7Yf-UbCs76yxSYg").build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(start_test, pattern='^start_test$'))
    application.add_handler(CallbackQueryHandler(handle_answer, pattern='^answer_'))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
