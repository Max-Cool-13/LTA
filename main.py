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
        "question": "Какое время суток тебе нравится больше всего?",
        "options": ["Утро", "День", "Вечер", "Ночь"],
        "image": "https://gas-kvas.com/uploads/posts/2023-01/1674168401_gas-kvas-com-p-vremya-sutok-den-risunok-1.jpg"
    },
    {
        "question": "Какое блюдо ты предпочитаешь на завтрак?",
        "options": ["Каша", "Яичница", "Бутерброд", "Блины"],
        "image": "https://pazlyigra.ru/uploads/posts/2022-03/tapeta-sniadanie-dla-ukochanej.jpg"
    },
    {
        "question": "Какой суп тебе больше нравится?",
        "options": ["Борщ", "Суп-пюре", "Окрошка", "Гороховый суп"],
        "image": "https://gagaru.club/uploads/posts/2023-06/1686014045_gagaru-club-p-sup-v-stolovoi-1.jpg"
    },
    {
        "question": "Какой салат тебе нравится?",
        "options": ["Салат Оливье", "Винегрет", "Салат Цезарь", "Свежие овощи"],
        "image": "https://mykaleidoscope.ru/x/uploads/posts/2022-10/1666336858_52-mykaleidoscope-ru-p-salat-pattaiya-instagram-55.jpg"
    },
    {
        "question": "Какое основное блюдо ты предпочитаешь?",
        "options": ["Котлеты", "Курица", "Плов", "Рыба"],
        "image": "https://i.pinimg.com/originals/bd/05/0e/bd050ea0b7b2ae02106958d7e063039a.jpg"
    },
    {
        "question": "Какой десерт тебе нравится больше всего?",
        "options": ["Пирожное", "Ватрушки", "Фрукты", "Кексы"],
        "image": "https://wallbox.ru/wallpapers/main2/201724/14975964515943822352b045.95649909.jpg"
    },
    {
        "question": "Какую кухню ты предпочитаешь?",
        "options": ["Русская", "Итальянская", "Кавказская", "Паназиатская"],
        "image": "https://bon-aventura.ru/800/600/https/i08.fotocdn.net/s116/06feee1a64708a14/public_pin_l/2651975975.jpg"
    },
    {
        "question": "Какой напиток ты предпочитаешь?",
        "options": ["Чай", "Кисель", "Какао", "Кефир"],
        "image": "https://konditer-optom.ru/wp-content/uploads/2019/08/3-bank-machine.png"
    },
    {
        "question": "Как ты относишься к острой пище?",
        "options": ["Люблю", "Нейтрально", "Не люблю", "Не пробовал"],
        "image": "https://gorets-media.ru/uploads/images/vestisgor/2019/August/.thumbs/73e9d0a66ed728caddf9f9916d5e56d8_1100_733_1.jpg"
    },
    {
        "question": "Какой тип перекуса ты предпочитаешь?",
        "options": ["Печенье", "Снэки", "Йогурт", "Орехи"],
        "image": "https://arena-swim.ru/wp-content/uploads/3/b/7/3b7de0de0c8e7f7d6cbf90ec626bbe21.jpeg"
    }
]

# Возможные результаты теста
results = {
    "Каша": "https://img.razrisyika.ru/kart/23/1200/89500-kasha-13.jpg",
    "Бутерброды с сыром": "https://klike.net/uploads/posts/2023-03/1678680534_2-2.jpg",
    "Запеканка": "https://adygsalt.ru/blog/foto/kartofelnie-zapekanki/1.jpg",
    "Плов": "https://bogatyr.club/uploads/posts/2023-06/1687857689_bogatyr-club-p-plov-v-kazane-foni-vkontakte-6.jpg",
    "Макароны с сосисками": "https://mykaleidoscope.ru/x/uploads/posts/2022-09/1663827932_23-mykaleidoscope-ru-p-spagetti-s-sosiskami-yeda-krasivo-24.jpg",
    "Котлеты": "https://klike.net/uploads/posts/2023-02/1677566609_3-13.jpg",
    "Борщ": "https://mykaleidoscope.ru/x/uploads/posts/2022-09/1663686606_11-mykaleidoscope-ru-p-borshch-so-smetanoi-oboi-15.jpg",
    "Салат из огурцов": "https://bee-garden.ru/800/600/https/ukrpublic.com/images/2020/12/30/Bk99VHySX_large.jpg",
    "Компот": "https://h3.amic.ru/images/upload/images_06-2019/images/kompot-klubnica.jpg",
    "Чай": "https://multiwood.ru/wp-content/uploads/2022/08/post_5cc16e65ddc17.jpg",
    "Оливье": "https://foodmood.ru/upload/iblock/3b5/3b5f7a1de0c320e76399b66ac653d615.jpg",
    "Творог": "https://kdpsaratov.ru/assets/templates/img/catalog/Vkusnii_den/Молокосодержащий%20продукт%20с%20шок%20крошкой_Бок.png",
    "Овощной салат": "http://klublady.ru/uploads/posts/2022-02/1644889472_11-klublady-ru-p-ovoshchnie-salati-foto-11.jpg",
    "Щи": "http://33kartoshki.ru/userfiles/images/novosti/image-1.jpg",
    "Макароны по-флотски": "https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_657df74b101eed21c7cd5240_657df8e09d9ff956347667c3/scale_1200",
}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()  # Сброс данных пользователя
    keyboard = [
        [InlineKeyboardButton("Начать тест", callback_data='start_test')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Готов узнать, какое блюдо из столовой тебе подойдёт? Жми "Начать тест"!', reply_markup=reply_markup)

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
