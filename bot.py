#! /user/bin/python3
from telegram import Bot, Update
from telegram.ext import *
from keys import token as bot_token
import datetime
import pytz

print('Starting up bot...')

group_chat_id = '-901580361'


def send_message(message):
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=group_chat_id, text=message)


def start_of_day_message():
    message = "Good morning! Have a wonderful day ahead!"
    send_message(message)


def middle_of_day_message():
    message = "Hello! Just a friendly reminder to take a break and relax!"
    send_message(message)


def end_of_day_message():
    message = "Good evening! Hope you had a productive day. Have a restful night!"
    send_message(message)


def start_command(update: Update, context):
    message = "Bot is started. Messages will be sent at specific times."
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))

    # Set the timezone to GMT+03:00
    timezone = pytz.timezone('Asia/Amman')

    # Create job queues for each message type
    job_queue = updater.job_queue

    # Define the message times in GMT+03:00 timezone
    start_time = datetime.time(hour=6, minute=0, tzinfo=timezone)
    middle_time = datetime.time(hour=10, minute=0, tzinfo=timezone)
    end_time = datetime.time(hour=21, minute=54, tzinfo=timezone)


    # Schedule the messages using run_daily method
    job_queue.run_daily(lambda context: start_of_day_message(), start_time, context=group_chat_id)
    job_queue.run_daily(lambda context: middle_of_day_message(), middle_time, context=group_chat_id)
    job_queue.run_daily(lambda context: end_of_day_message(), end_time, context=group_chat_id)

    
    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()