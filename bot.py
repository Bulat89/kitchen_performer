import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import logging
from database import add_user, create_users_table

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# States for conversation
(FIRST_NAME, LAST_NAME, PATRONYMIC, CUSTOMER_PHONE, CONTACT_PHONE,
 ORGANIZATION_NAME, SOCIAL_MEDIA_CHOICE, SOCIAL_MEDIA_HANDLE) = range(8)

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks for the user's first name."""
    update.message.reply_text(
        'Здравствуйте! Я бот для регистрации новых пользователей. '
        'Давайте начнем. Введите ваше имя.'
    )
    return FIRST_NAME

def first_name(update: Update, context: CallbackContext) -> int:
    """Stores the first name and asks for the last name."""
    context.user_data['first_name'] = update.message.text
    update.message.reply_text('Спасибо! Теперь введите вашу фамилию.')
    return LAST_NAME

def last_name(update: Update, context: CallbackContext) -> int:
    """Stores the last name and asks for the patronymic."""
    context.user_data['last_name'] = update.message.text
    update.message.reply_text('Отлично! Введите ваше отчество.')
    return PATRONYMIC

def patronymic(update: Update, context: CallbackContext) -> int:
    """Stores the patronymic and asks for the customer phone."""
    context.user_data['patronymic'] = update.message.text
    update.message.reply_text('Теперь введите ваш телефон для связи (с заказчиком).')
    return CUSTOMER_PHONE

def customer_phone(update: Update, context: CallbackContext) -> int:
    """Stores the customer phone and asks for the contact phone."""
    context.user_data['customer_phone'] = update.message.text
    update.message.reply_text('Спасибо. А теперь телефон для связи с нами.')
    return CONTACT_PHONE

def contact_phone(update: Update, context: CallbackContext) -> int:
    """Stores the contact phone and asks for the organization name."""
    context.user_data['contact_phone'] = update.message.text
    update.message.reply_text('Введите название вашей организации.')
    return ORGANIZATION_NAME

def organization_name(update: Update, context: CallbackContext) -> int:
    """Stores the organization name and asks for social media choice."""
    context.user_data['organization_name'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Instagram", callback_data='Instagram')],
        [InlineKeyboardButton("VK", callback_data='VK')],
        [InlineKeyboardButton("Telegram", callback_data='Telegram')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите социальную сеть для привязки:', reply_markup=reply_markup)
    return SOCIAL_MEDIA_CHOICE

def social_media_choice(update: Update, context: CallbackContext) -> int:
    """Stores the social media platform and asks for the handle."""
    query = update.callback_query
    query.answer()
    context.user_data['social_media_platform'] = query.data
    query.edit_message_text(text=f"Вы выбрали: {query.data}. Теперь введите ваш ник или ID.")
    return SOCIAL_MEDIA_HANDLE

def social_media_handle(update: Update, context: CallbackContext) -> int:
    """Stores the social media handle, saves user data, and ends the conversation."""
    context.user_data['social_media_handle'] = update.message.text

    # Save to database
    if add_user(context.user_data):
        update.message.reply_text('Спасибо! Ваша регистрация завершена.', reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text('Произошла ошибка при сохранении данных. Попробуйте позже.', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    update.message.reply_text(
        'Регистрация отменена.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

from dotenv import load_dotenv

def main() -> None:
    """Run the bot."""
    # Load environment variables from .env file
    load_dotenv()

    # Create the 'users' table if it doesn't exist
    create_users_table()

    # Get the token from environment variables
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set.")
        return

    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST_NAME: [MessageHandler(Filters.text & ~Filters.command, first_name)],
            LAST_NAME: [MessageHandler(Filters.text & ~Filters.command, last_name)],
            PATRONYMIC: [MessageHandler(Filters.text & ~Filters.command, patronymic)],
            CUSTOMER_PHONE: [MessageHandler(Filters.text & ~Filters.command, customer_phone)],
            CONTACT_PHONE: [MessageHandler(Filters.text & ~Filters.command, contact_phone)],
            ORGANIZATION_NAME: [MessageHandler(Filters.text & ~Filters.command, organization_name)],
            SOCIAL_MEDIA_CHOICE: [CallbackQueryHandler(social_media_choice)],
            SOCIAL_MEDIA_HANDLE: [MessageHandler(Filters.text & ~Filters.command, social_media_handle)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()