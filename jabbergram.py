#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sleekxmpp
import telegram
import logging
import configparser
from threading import Thread
from queue import Queue
from telegram.error import NetworkError, Unauthorized
from time import sleep
from sys import argv


class EchoBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, room, nick, token, group):
        # XMPP
        super(EchoBot, self).__init__(jid, password)
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('groupchat_message', self.muc_message)
        self.muc_room = room
        self.nick = nick
        self.token = token

        # Telegram
        self.group = group
        self.bot = telegram.Bot(self.token)

        # meter el conecto del tg en un hilo
        t = Thread(target=self.read_tg)
        t.daemon = True
        t.start()

        # activar logueo basico
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        logger = logging.getLogger(__name__)

    def read_tg(self):
        update_id = 0

        while True:
            try:
                for update in self.bot.getUpdates(offset=update_id,
                                                      timeout=10):
                    update_id = update.update_id + 1
                    message = update.message.text
                    user = str(update.message.from_user.username)
                    if not user:
                        user = str(update.message.from_user.first_name)
                    if not user:
                        user = "Unidentified: "
                    mensaje = user + ": " + message
                    chat_id = update.message.chat_id

                    if message and chat_id == self.group:
                        self.send_message(mto=self.muc_room,
                                              mbody=mensaje,
                                              mtype='groupchat')
            except NetworkError:
                sleep(1)
            except Unauthorized:
                update_id += 1

    def start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.muc_room, self.nick, wait=True)

    def muc_message(self, msg):
        print(msg)
        if msg['mucnick'] != self.nick:
            mensaje = str(msg['from']).split('/')[1] + ': ' + str(msg['body'])
            print(mensaje)
            self.bot.sendMessage(self.group, text=mensaje)
            print("fuera")

if __name__ == '__main__':

    # parsear config
    config = []
    parser = configparser.SafeConfigParser()

    if len(argv) == 2:
        parser.read(argv[1])
    else:
        parser.read('config.ini')

    for name, value in parser.items('config'):
        config.append(value)

    # asignar valores para el bot
    jid = config[0]
    password = config[1]
    muc_room = config[2]
    nick = config[3]
    token = config[4]
    group = int(config[5])

    xmpp = EchoBot(jid, password, muc_room, nick, token, group)
    xmpp.register_plugin('xep_0045')

    if xmpp.connect():
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")

    # Vols un gram nen?
