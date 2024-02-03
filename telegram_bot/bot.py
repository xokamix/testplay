from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = '6474234096:AAGlt7B7jicTa6UGuomO1z1R0trmVzLRET0'
BACKEND_API_URL = 'http://localhost:8000/api/'
API_TOKEN = 'YOUR_API_TOKEN'

def start(update, context):
    update.message.reply_text('Welcome to the LetsPlay Telegram bot! Use /lessons to list your lessons.')

def lessons(update, context):
    headers = {'Authorization': f'Token {API_TOKEN}'}
    try:
        response = requests.get(f'{BACKEND_API_URL}lessons/', headers=headers)
        if response.status_code == 200:
            lessons_list = response.json()
            reply_text = 'Your Lessons:\n' + '\n'.join([f"Title: {lesson['title']}, Schedule: {lesson['schedule']}" for lesson in lessons_list])
            update.message.reply_text(reply_text)
        else:
            logger.error('Failed to fetch lessons. Status code: %s', response.status_code)
            update.message.reply_text('Failed to fetch lessons.')
    except Exception as e:
        logger.error('Error fetching lessons: %s', str(e))
        update.message.reply_text('An error occurred while fetching lessons.')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("lessons", lessons))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
