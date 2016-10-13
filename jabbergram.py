#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    import requests
except:
    print("HTTP Upload support disabled.")
import sleekxmpp
import telegram
import configparser
from threading import Thread
from queue import Queue
from telegram.error import NetworkError, Unauthorized
from time import sleep
from sys import argv
from sys import exit
from sleekxmpp.xmlstream.stanzabase import ElementBase
from sleekxmpp.stanza.iq import Iq
from xml.dom import minidom


class Request(ElementBase):
    namespace = 'urn:xmpp:http:upload'
    name = 'request'
    plugin_attrib = 'request'
    interfaces = set(('filename', 'size'))
    sub_interfaces = interfaces

class Jabbergram(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, rooms, nick, token, groups):
        # XMPP
        super(Jabbergram, self).__init__(jid, password)
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('groupchat_message', self.muc_message)

        self.muc_rooms = rooms.split()
        self.nick = nick
        self.token = token
        self.xmpp_users = {}
        self.jid = jid

        for muc in self.muc_rooms:
            self.add_event_handler("muc::%s::got_online" % muc,
                                   self.muc_online)
            self.add_event_handler("muc::%s::got_offline" % muc,
                                   self.muc_offline)

        # Telegram
        self.groups = groups.split()
        self.bot = telegram.Bot(self.token)
        self.telegram_users = {}

        # initialize http upload on a thread since its needed to be connected
        # to xmpp
        t = Thread(target=self.init_http)
        t.daemon = True
        t.start()

        # put tg connector in a thread
        t = Thread(target=self.read_tg)
        t.daemon = True
        t.start()

        print('Please wait a couple of minutes until it\'s correctly '
              'connected')

    def init_http(self):
        self.http_upload = self.HttpUpload(self)
        self.component = self.http_upload.discovery()

        if self.component:
            xml = self.http_upload.disco_info(self.component)
            xml = minidom.parseString(str(xml))
            self.max_size = int(xml.getElementsByTagName('value')
                                [1].firstChild.data)
        else:
            try:
                self.component = self.jid.split('@')[1]
                xml = self.http_upload.disco_info(self.component)
                xml = minidom.parseString(str(xml))
                self.max_size = int(xml.getElementsByTagName('value')
                                    [1].firstChild.data)
            except:
                self.max_size = None

    def read_tg(self):
        update_id = 0

        # wait until http_upload has been tested
        sleep(5)
        while True:
            try:
                for update in self.bot.getUpdates(offset=update_id,
                                                  timeout=10):

                    if update.message.audio or update.message.document or \
                       update.message.photo or update.message.video \
                       or update.message.voice:

                        # proceed only if http upload is available
                        if self.max_size is not None:
                            if update.message.audio:
                                d_file = update.message.audio
                                ext = '.ogg'
                                size = d_file.file_size
                            elif update.message.document:
                                d_file = update.message.document
                                ext = ''
                                size = d_file.file_size
                            elif update.message.photo:
                                d_file = update.message.photo[-1]
                                ext = '.jpg'
                                size = d_file.file_size
                            elif update.message.video:
                                d_file = update.message.video[-1]
                                ext = '.mp4'
                                size = d_file.file_size
                            elif update.message.voice:
                                d_file = update.message.voice
                                ext = '.ogg'
                                size = d_file.file_size
                            if self.max_size >= size:
                                t_file = self.bot.getFile(d_file.file_id)
                                name = '/tmp/' + d_file.file_id + ext
                                t_file.download(name)
                                url = self.http_upload.upload(
                                                              self.component,
                                                              '', name, size)

                                if update.message.caption:
                                    message = update.message.caption + ' '
                                else:
                                    message = 'File uploaded: '

                                message += url
                            else:
                                message = 'A file has been uploaded to Telegra'
                                'm, but is too big.'
                        else:
                            message = 'A file has been uploaderd to Telegram, '
                            'but the XMPP server doesn\'t support HTTP Upload.'

                    elif update.message.new_chat_member:
                        message = 'This user has joined the group.'
                    elif update.message.left_chat_member:
                        message = 'This user has left the group.'
                    elif update.message.new_chat_title:
                        message = 'The group\'s title has changed: '+ \
                          update.message.new_chat_title
                    elif update.message.new_chat_photo:
                        message = 'The group\'s photo haschanged.'
                    else:
                        message = update.message.text

                    user = str(update.message.from_user.username)

                    # sometimes there's no user. weird, but it happens
                    if not user:
                        user = str(update.message.from_user.first_name)

                    # even weirder is that username or first_name exists
                    # let's take last_name
                    if not user:
                        user = str(update.message.from_user.last_name)

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
                print(e)
                sleep(1)

            except Unauthorized:
                print(e)
                sleep(1)

            except Exception as e:
                update_id += 1
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

        elif service == 'telegram':
            self.bot.sendMessage(group, text=message)

    class HttpUpload():
        def __init__(self, parent_self):
            self.parent_self = parent_self

        def discovery(self):

            disco = sleekxmpp.basexmpp.BaseXMPP.Iq(self.parent_self)
            disco['query'] = "http://jabber.org/protocol/disco#items"
            disco['type'] = 'get'
            disco['from'] = self.parent_self.jid
            disco['to'] = self.parent_self.jid.split('@')[1]

            d = disco.send(timeout=30)
            xml = minidom.parseString(str(d))
            item = xml.getElementsByTagName('item')

            for component in item:
                component = component.getAttribute('jid')
                info = self.disco_info(component)

                if "urn:xmpp:http:upload" in info:
                    http_upload_component = component
                    break
                else:
                    http_upload_component = ""

            return http_upload_component

        def disco_info(self, component):

            info = sleekxmpp.basexmpp.BaseXMPP.Iq(self.parent_self)
            info['query'] = "http://jabber.org/protocol/disco#info"
            info['type'] = 'get'
            info['from'] = self.parent_self.jid
            info['to'] = component

            return str(info.send(timeout=30))

        def upload(self, component, verify_ssl, u_file, size):

            peticion = Request()
            peticion['filename'] = u_file.split('/')[-1]
            peticion['size'] = str(size)

            iq = sleekxmpp.basexmpp.BaseXMPP.Iq(self.parent_self)
            iq.set_payload(peticion)
            iq['type'] = 'get'
            iq['to'] = component
            iq['from'] = self.parent_self.jid

            send = iq.send(timeout=30)

            xml = minidom.parseString(str(send))
            put_url = xml.getElementsByTagName('put')[0].firstChild.data

            verify_ssl = ''
            if verify_ssl == 'False':
                req = requests.put(put_url, data=open(u_file, 'rb'),
                                   verify=False)
            else:
                req = requests.put(put_url, data=open(u_file, 'rb'))

            return put_url


if __name__ == '__main__':

    # parse config
    config = []
    parser = configparser.SafeConfigParser()

    if len(argv) == 2:
        parser.read(argv[1])
    else:
        parser.read('config.ini')

    for name, value in parser.items('config'):
        config.append(value)

    # assign values for the bot
    jid = config[0]
    password = config[1]
    muc_rooms = config[2]
    nick = config[3]
    token = config[4]
    groups = config[5]

    xmpp = Jabbergram(jid, password, muc_rooms, nick, token, groups)
    xmpp.register_plugin('xep_0045')

    if xmpp.connect():
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")

    # Vols un gram nen?
