#! /user/bin/python3
from telegram import Bot, Update
from ctf_times_utils import *
from telegram.ext import *
from keys import token as bot_token
import traceback
import datetime
from time import *
import pytz

print('Starting up bot...')

# group_chat_id = '-901580361'
group_chat_id ='-1001904108964'

commands_msg = '''
/start امر لتشغيل البوت
/commands الاوامر المتوفرة في البوت
/upcomming_CTF مسابقات امسك العلم القادمة في الخمس ايام القادمة
/help عرض المساعدة 
'''

# Log errors
def error(update, context):
    traceback.print_exc()    
    print(f'Update {update} caused error {context.error}')

# Lets us use the /help command
def help_command(update, context):
    update.message.reply_text(commands_msg)

def upcomming_CTF(update, context):
    for counter , event in enumerate(incomming_events_list_wrapper()):
        if counter % 5 == 0 :
            sleep(2)
        update.message.reply_text('\n'.join([part for part in event]) ,timeout=900) 

def commands(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=commands_msg)

def send_message(message):
    bot = Bot(token=bot_token)
    # bot.send_message(chat_id=group_chat_id, text=message)
    for counter , event in enumerate(incomming_events_list_wrapper()):
        if counter % 3 == 0 :
            sleep(8)
        bot.send_message(chat_id=group_chat_id, text='\n'.join([part for part in event]) ,timeout=900)

def start_of_day_message():
    message = "Good morning! Have a wonderful day ahead!"
    send_message(message)

def middle_of_day_message():
    message = "Hello! Just a friendly reminder to take a break and relax!"
    send_message(message)

def end_of_day_message():
    message = "Good evening! Hope you had a productive day. Have a restful night!"
    send_message(message)

def start_command(update, context):
    message = "Bot is started. Messages will be sent at specific times."
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    # Log all errors
    dp.add_error_handler(error)
    
    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('commands', commands))
    dp.add_handler(CommandHandler('upcomming_CTF', upcomming_CTF))
    dp.add_handler(CommandHandler('help', help_command))

    # Set the timezone to GMT+03:00
    timezone = pytz.timezone('Asia/Amman')

    # Create job queues for each message type
    job_queue = updater.job_queue

    # Define the message times in GMT+03:00 timezone
    start_time = datetime.time(hour=7, minute=0, tzinfo=timezone)
    # middle_time = datetime.time(hour=13, minute=0, tzinfo=timezone)
    # end_time = datetime.time(hour=21, minute=0, tzinfo=timezone)


    # Schedule the messages using run_daily method
    job_queue.run_daily(lambda context: start_of_day_message(), start_time, context=group_chat_id)
    # job_queue.run_daily(lambda context: middle_of_day_message(), middle_time, context=group_chat_id)
    # job_queue.run_daily(lambda context: end_of_day_message(), end_time, context=group_chat_id)

    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()