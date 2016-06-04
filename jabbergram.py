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
    def __init__(self, jid, password, rooms, nick, token, groups):
        # XMPP
        super(EchoBot, self).__init__(jid, password)
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('groupchat_message', self.muc_message)

        self.muc_rooms = rooms.split()
        self.nick = nick
        self.token = token
        self.xmpp_users = {}

        for muc in self.muc_rooms:
            self.add_event_handler("muc::%s::got_online" % muc,
                                self.muc_online)
            self.add_event_handler("muc::%s::got_offline" % muc,
                                self.muc_offline)

        # Telegram
        self.groups = groups.split()
        self.bot = telegram.Bot(self.token)
        self.telegram_users = {}

        # meter el conector del tg en un hilo
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

                    # sometimes there's no user. weird, but it happens
                    if not user:
                        user = str(update.message.from_user.first_name)

                    msg = user + ": " + message
                    chat_id = update.message.chat_id

                    if message and str(chat_id) in self.groups:
                        index = self.groups.index(str(chat_id))
                        receiver = self.muc_rooms[index]

                        if chat_id in self.telegram_users:
                            if user not in self.telegram_users[chat_id]:
                                self.telegram_users[chat_id] += ' ' + user
                        else:
                            self.telegram_users[chat_id] = ' ' + user

                        if message == '.users':
                            index = self.groups.index(str(chat_id))
                            muc = self.muc_rooms[index]
                            self.say_users('telegram', muc, chat_id)
                        else:
                            self.send_message(mto=receiver, mbody=msg,
                                                mtype='groupchat')
                    update_id = update.update_id + 1

            except NetworkError as e:
                sleep(1)

            except Unauthorized:
                sleep(1)

            except Exception as e:
                print(e)


    def start(self, event):
        self.get_roster()
        self.send_presence()

        for muc in self.muc_rooms:
            self.plugin['xep_0045'].joinMUC(muc, self.nick, wait=True)

    def muc_message(self, msg):
        muc_room = str(msg['from']).split('/')[0]
        index = self.muc_rooms.index(muc_room)
        tg_group = self.groups[index]

        if msg['body'] == '.users':
            self.say_users('xmpp', muc_room, tg_group)

        elif msg['mucnick'] != self.nick:
            message = str(msg['from']).split('/')[1] + ': ' + str(msg['body'])
            self.bot.sendMessage(tg_group, text=message)

    def muc_online(self, presence):
        user = presence['muc']['nick']
        muc = presence['from'].bare

        if user != self.nick:
            if muc in self.xmpp_users:
                self.xmpp_users[muc].append(presence['muc']['nick'])
            else:
                self.xmpp_users[muc] = [presence['muc']['nick']]

    def muc_offline(self, presence):
        user = presence['muc']['nick']
        muc = presence['from'].bare

        if user != self.nick:
            self.xmpp_users[muc].remove(presence['muc']['nick'])

    def say_users(self, service, muc, group):
        xmpp_users = ""
        tg_users = ""
        group = int(group)

        if muc in self.xmpp_users:
            for i in self.xmpp_users[muc]:
                xmpp_users = xmpp_users + ' _' + i
        else:
            xmpp_users = ""

        msg1 = 'XMPP Users:' + xmpp_users

        if group in self.telegram_users:
            tg_users = self.telegram_users[group]
        else:
            tg_users = ""

        msg2 = 'Telegram Users:' + tg_users

        message = msg1 + '\n' + msg2

        if service == 'xmpp':
            self.send_message(mto=muc, mbody=message, mtype='groupchat')
        # arreglar el .users por el lado de tg
        elif service == 'telegram':
            self.bot.sendMessage(group, text=message)


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
    muc_rooms = config[2]
    nick = config[3]
    token = config[4]
    groups = config[5]

    xmpp = EchoBot(jid, password, muc_rooms, nick, token, groups)
    xmpp.register_plugin('xep_0045')

    if xmpp.connect():
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")

    # Vols un gram nen?
