import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    CallbackQueryHandler, 
    MessageHandler, 
    filters,  
    ContextTypes
)
import asyncio

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Список страшных историй с текстами
scary_stories = {
    "Дико страшная история": "Дело было ночью, кот, как обычно спал в ногах. Я тоже заснула...",
    "Спиритизм и его последствия!": "Моя одна знакомая, со своими подругами, подвыпив, решили вызвать духа Пушкина...",
    "Игра в смерть": "Ох, это лучше и не рассказывать, всё равно не поверят...",
    "Домовой": "Мне было 15, троюродному брату 16...",
    "Кого видят дети?": "Однажды — мне было шесть лет — я проснулся будто от толчка...",
    "Чёрный кот": "Мы тогда жили в Казахстане. У нас был большой дом..."
}

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} начал общение с ботом.")
    
    # Создание кнопок с обновлённым текстом
    keyboard = [
        [InlineKeyboardButton("Тогда начнём нашу игру, путник", callback_data='start_game')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Плохо утра или ночи, {user.first_name}! Привет! Выберите действие:", reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Подтверждение нажатия кнопки

    if query.data == 'start_game':
        # Создание новых кнопок после начала игры
        keyboard = [
            [InlineKeyboardButton("Желаете услышать страшные истории?", callback_data='scary_stories')],
            [InlineKeyboardButton("Сыграете с демонами в карты?", callback_data='play_cards')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Игра началась! Что вы хотите сделать?", reply_markup=reply_markup)

    elif query.data == 'scary_stories':
        # Создание кнопок для выбора историй
        keyboard = [
            [InlineKeyboardButton("Дико страшная\nистория", callback_data="Дико страшная история")],
            [InlineKeyboardButton("Спиритизм и его\nпоследствия!", callback_data="Спиритизм и его последствия!")],
            [InlineKeyboardButton("Игра в\nсмерть", callback_data="Игра в смерть")],
            [InlineKeyboardButton("Домовой", callback_data="Домовой")],
            [InlineKeyboardButton("Кого видят\nдети?", callback_data="Кого видят дети?")],
            [InlineKeyboardButton("Чёрный кот", callback_data="Чёрный кот")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Выберите историю, которую хотите услышать:", reply_markup=reply_markup)

    elif query.data in scary_stories:
        # Отправка текста выбранной истории и вывод новых кнопок
        story_text = scary_stories[query.data]
        
        # Кнопки для выбора действий после прочтения истории
        keyboard = [
            [InlineKeyboardButton("Выбрать другую историю", callback_data='scary_stories')],
            [InlineKeyboardButton("Перейти в игру", callback_data='play_cards')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Отправка текста истории и вывод новых кнопок
        await query.edit_message_text(text=story_text, reply_markup=reply_markup)

    elif query.data == 'play_cards':
        await query.edit_message_text(text="Вы начали играть в карты с демонами... (добавьте текст игры)")

# Обработка всех текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Если сообщение не является командой /start, то отправляем приветственное сообщение с кнопкой
    if update.message.text and update.message.text.lower() != "/start":
        await start(update, context)

# Основная функция для запуска бота
async def main():
    # Токен, полученный от BotFather
    token = "8059647384:AAGE9ZdbgtP1y8A2-srR20yNey6nm6SeCsc"
    
    # Создаем приложение
    application = ApplicationBuilder().token(token).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))  # Обработчик для кнопок
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))  # Обработчик для текстовых сообщений
    
    # Запускаем бота
    logger.info("Запуск бота...")
    
    # Инициализация и запуск приложения
    await application.initialize()
    await application.start()
    
    # Ожидаем поступления обновлений
    await application.updater.start_polling()
    
    logger.info("Бот работает...")
    
    # Ожидание, пока не будет вызван сигнал остановки
    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        # Проверяем существование активного цикла событий
        try:
            loop = asyncio.get_running_loop()
            loop.run_until_complete(main())
        except RuntimeError:  # Если нет активного цикла событий, создаем новый
            asyncio.run(main())
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
