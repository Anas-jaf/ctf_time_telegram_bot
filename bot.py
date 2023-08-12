#!/bin/python3
from keys import token as bot_token
from telegram import Bot, Update
from ctf_times_utils import *
from telegram.ext import *
from time import *
import traceback
import datetime
import pytz
import glob

print('Starting up bot...')

# group_chat_id = '-901580361'
group_chat_id ='-1001904108964'
# group_chat_id ='-1904108964'

commands_msg = '''
/start امر لتشغيل البوت
/commands الاوامر المتوفرة في البوت
/upcoming مسابقات امسك العلم القادمة في الخمس ايام القادمة
/help عرض المساعدة 
'''

def send_pdf_to_group(chat_id=group_chat_id):
    bot = Bot(token=bot_token)
    output_path = './send_folder/latest_CTF_competetions.pdf'
    create_pdf_from_dictionary_list(output_path, get_incomming_events())    
    files = count_files()
    send_files(bot , chat_id ,files)
    delete_send_folder()

def send_files(bot, chat_id, files , outdir='./send_folder',name="ملف مضغوظ"):
    for file in files:
        bot.send_document(chat_id=chat_id, document=open(file, 'rb'), timeout=9000)

# Log errors
def error(update, context):
    traceback.print_exc()    
    print(f'Update {update} caused error {context.error}')
    if update is not None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'ERROR: Update {update} caused error {context.error}')
    else:
        # Handle the case when update is None
        print("Error: Update is None.")

# Lets us use the /help command
def help_command(update, context):
    update.message.reply_text(commands_msg)

def upcoming_CTF(update, context): 
    update.message.reply_text("انتظر لو سمحت") 
    chat_id = update.message.chat.id
    send_message(chat_id)

def commands(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=commands_msg)

def send_message(chat_id =group_chat_id):
    bot = Bot(token=bot_token)
    for counter , event in enumerate(incomming_events_list_wrapper()):
        if counter % 5 == 0 :
            sleep(2)
        bot.send_message(chat_id=chat_id, text='\n'.join([part for part in event]) ,timeout=900)

def start_of_day_message():
    message = "Good morning! Have a wonderful day ahead!"
    send_message()
    # send_pdf_to_group()

def middle_of_day_message():
    message = "Hello! Just a friendly reminder to take a break and relax!"
    send_message()
    # send_pdf_to_group()

def end_of_day_message():
    message = "Good evening! Hope you had a productive day. Have a restful night!"
    send_message()
    # send_pdf_to_group()

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
    dp.add_handler(CommandHandler('upcoming', upcoming_CTF))
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