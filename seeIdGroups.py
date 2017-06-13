#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telegram
import configparser
from telegram.error import NetworkError, Unauthorized
from time import sleep
from sys import argv


parser = configparser.SafeConfigParser()
parser.read(argv[1] if len(argv) == 2 else 'config.ini')
config = parser['config']
bot = telegram.Bot(config['token'])

update_id = 0
print('It can take a while to print the ID, please wait.')
print("Press Ctrl-c when the ID you want is printed.")

printed = []

while True:
    try:
        for update in bot.getUpdates(offset=update_id, timeout=10):
            chat_id = update.message.chat_id
            chat_title = update.message
            if chat_id not in printed:
                printed.append(chat_id)
                print("Title: " + str(chat_title['chat']['title']))
                print("ID: " + str(chat_id))
    except NetworkError:
        sleep(1)
    except Unauthorized:
        update_id += 1
