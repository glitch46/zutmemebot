from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

import random
import os
import time
import schedule
import threading

import settings

bot = telegram.Bot(token=settings.BOT_TOKEN)
updater = Updater(token=settings.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello, I'm bot for sending memes\n add me as an admin to channel and add it's name to settings")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()


def send_meme(meme_filename, channel_name):
    meme_image = open(meme_filename, "rb")
    bot.send_photo(chat_id=channel_name, photo=meme_image)


def send_text(msg, channel_name):
    bot.send_message(chat_id=channel_name, text=msg)


def process_new_meme(folder, channel_name):
    try:
        print(f"PROCESSING FOLDER {folder} CHANNEL {channel_name}")
        gauth = GoogleAuth()

        gauth.LoadCredentialsFile("creds.txt")

        if gauth.credentials is None:
            gauth.GetFlow()
            gauth.flow.params.update({'access_type': 'offline'})
            gauth.flow.params.update({'approval_prompt': 'force'})
            gauth.LocalWebserverAuth()

        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
        gauth.SaveCredentialsFile("creds.txt")
        drive = GoogleDrive(gauth)

        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

        memes_folder_id = None
        for file1 in file_list:
            if file1['title'] == folder:
                memes_folder_id = file1['id']
                break

        if not memes_folder_id:
            print(f"{folder} FOLDER NOT FOUND")

        else:
            memes_list = drive.ListFile({'q': f"'{memes_folder_id}' in parents and trashed=false"}).GetList()

            for meme in memes_list:
                print(f"title: {meme['title']}, id: {meme['id']}")
            selected_meme = random.choice(memes_list)

            meme_file = drive.CreateFile({'id': selected_meme['id']})
            meme_file.GetContentFile("./memes/" + selected_meme['title'])
            send_meme("./memes/" + selected_meme['title'], channel_name)
            os.remove("./memes/" + selected_meme['title'])
    except Exception as e:
        print(e)


# TODO it's needed to find the way hot to run tasks in the loop
try:
    schedule.every(settings.tasks[0][2]).seconds.do(
        lambda: process_new_meme(settings.tasks[0][0], settings.tasks[0][1]))
except:
    pass

try:
    schedule.every(settings.tasks[1][2]).seconds.do(
        lambda: process_new_meme(settings.tasks[1][0], settings.tasks[1][1]))
except:
    pass

try:
    schedule.every(settings.tasks[2][2]).seconds.do(
        lambda: process_new_meme(settings.tasks[2][0], settings.tasks[2][1]))
except:
    pass

try:
    schedule.every(settings.tasks[3][2]).seconds.do(
        lambda: process_new_meme(settings.tasks[3][0], settings.tasks[3][1]))
except:
    pass

try:
    schedule.every(settings.tasks[4][2]).seconds.do(
        lambda: process_new_meme(settings.tasks[4][0], settings.tasks[4][1]))
except:
    pass

try:
    schedule.every(settings.tasks[5][2]).seconds.do(
        lambda: process_new_meme(settings.tasks[5][0], settings.tasks[5][1]))
except:
    pass

try:
    schedule.every(settings.tasks[6][2]).seconds.do(
        lambda: process_new_meme(settings.tasks[6][0], settings.tasks[6][1]))
except:
    pass

while 1:
    schedule.run_pending()
    time.sleep(1)
