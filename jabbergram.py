#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sleekxmpp
import telegram
import configparser
from threading import Thread
from queue import Queue
from telegram.error import NetworkError, Unauthorized
from time import sleep
from sys import argv
from sys import exit


class EchoBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, room, nick, token, group):
        # XMPP
        super(EchoBot, self).__init__(jid, password)
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('groupchat_message', self.muc_message)
        self.add_event_handler("muc::%s::got_online" % room,
                               self.muc_online)
        self.add_event_handler("muc::%s::got_offline" % room,
                               self.muc_offline)

        self.muc_room = room
        self.nick = nick
        self.token = token
        self.xmpp_users = []

        # Telegram
        self.group = group
        self.bot = telegram.Bot(self.token)
        self.telegram_users = []

        # meter el conecto del tg en un hilo
        t = Thread(target=self.read_tg)
        t.daemon = True
        t.start()

        print('Please wait a couple of minutes until it\'s correctly '
                  'connected')

    def read_tg(self):
        update_id = 0

        while True:
            try:
                for update in self.bot.getUpdates(offset=update_id,
                                                      timeout=10):
                    message = update.message.text
                    user = str(update.message.from_user.username)

                    if not user:
                        user = str(update.message.from_user.first_name)

                    msg = user + ": " + message
                    chat_id = update.message.chat_id

                    if message and chat_id == self.group:
                        if user not in self.telegram_users:
                            self.telegram_users.append(user)

                        if message == '.users':
                            self.say_users('telegram')

                        else:
                            self.send_message(mto=self.muc_room,
                                                mbody=msg,
                                                mtype='groupchat')

                    update_id = update.update_id + 1

            except NetworkError:
                sleep(1)
            except Unauthorized:
                sleep(1)

    def start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.muc_room, self.nick, wait=True)

    def muc_message(self, msg):
        if msg['body'] == '.users':
            self.say_users('xmpp')

        elif msg['mucnick'] != self.nick:
            message = str(msg['from']).split('/')[1] + ': ' + str(msg['body'])
            self.bot.sendMessage(self.group, text=message)


    def muc_online(self, presence):
        if presence['muc']['nick'] != self.nick:
            self.xmpp_users.append(presence['muc']['nick'])

    def muc_offline(self, presence):
        if presence['muc']['nick'] != self.nick:
            self.xmpp_users.remove(presence['muc']['nick'])

    def say_users(self, service):
        xmpp_users = ""
        tg_users = ""

        for i in self.xmpp_users:
            xmpp_users = xmpp_users + ' _' + i

        msg1 = 'XMPP Users:' + xmpp_users

        for i in self.telegram_users:
            tg_users = tg_users + ' ' + i

        if not tg_users:
            tg_users = ""

        msg2 = 'Telegram Users:' + tg_users

        message = msg1 + '\n' + msg2

        if service == 'xmpp':
            self.send_message(mto=self.muc_room,
                                mbody=message,
                                mtype='groupchat')
        elif service == 'telegram':
            self.bot.sendMessage(self.group, text=message)

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
