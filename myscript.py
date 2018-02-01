
#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import select
import yaml
import re
import smtplib
import socket
import config
import telebot
from email.message import EmailMessage
from systemd import journal
from systemd.journal import JournalHandler

#conf = yaml.load(open('conf.yaml'))
bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=["text"])
def send_telegram(message, dandt, level, hellp, from_who): # Название функции не играет никакой роли, в принципе
    mes = "\r\n".join((
        "Уровень угрозы: %s" % level,
        "IP компьютера: %s" % from_who,
        "Дата и время: %s" % dandt,
        "Проблема: %s" % message,
        "Способы решения: %s" % hellp
    ))
    bot.send_message(129369755, mes)
    
def send_email(message, level, from_who, dandt, hellp):
    print('input function emai')
    me = 'python@mydomain.com'
    you = 'yuriy@fastzone.ru'
#    you = conf[0]['email']
    print(you + 'meil from config')
    msg = EmailMessage()
    mes = "\r\n".join((
        "Уровень угрозы: %s" % level,
        "IP компьютера: %s" % from_who,
        "Дата и время: %s" % dandt,
        "Проблема: %s" % message,
        "Способы решения: %s" % hellp
    ))
    msg.set_content(mes)
    msg['Subject'] = 'Level' + ' ' + level
    msg['From'] = me
    msg['To'] = you
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    print('output function emai')
    s.quit()

def test_event (myevent, level):    
    j = journal.Reader()
    j.this_boot()
#    j.log_level(journal.LOG_INFO)
    level
#    j.log_level(journal.level)
    j.add_match(MESSAGE = myevent)
    for entry in j:                                 
        print(str(entry['__REALTIME_TIMESTAMP'] )+ ' ' + entry['MESSAGE'])

def output_event_in_real_time(massevent):
    j = journal.Reader()
    j.log_level(journal.LOG_INFO)
    j.seek_tail()
    j.get_previous()    
    p = select.poll()
    p.register(j, j.get_events())
    while p.poll(): 
        for entry in j:
            i = 0
            while i < len(massevent): 
                event = re.compile(massevent[i]['regexp'])
                result  = event.findall(entry['MESSAGE'])
                if result:
                    if (massevent[i]['happened'] + 1) >= (massevent[i]['limit']):
                        print(str(entry['__REALTIME_TIMESTAMP']) + ' ' + result[0])
                        from_who = socket.gethostbyname(socket.gethostname())
                        send_email(result[0], massevent[i]['priority'], from_who, str(entry['__REALTIME_TIMESTAMP']), massevent[i]['help'])
                        send_telegram(result[0], str(entry['__REALTIME_TIMESTAMP']), massevent[i]['priority'], massevent[i]['help'], from_who)
                        print('Send message administrator from: ' + from_who)
                        massevent[i]['happened'] == 0
                    else:
                        massevent[i]['happened'] += 1
                i += 1

#send_email('send message', 'red', 'yuriy@fastzone.ru')

#level = conf[0]['email']
#test_event('fatal: no SASL authentication mechanisms', level)
cfg = yaml.load(open('database.yaml'))
output_event_in_real_time (cfg)