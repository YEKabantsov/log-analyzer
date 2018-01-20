
#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import select
import yaml
import re
from systemd import journal
from systemd.journal import JournalHandler



#import smtplib   
#s = smtplib.SMTP("localhost")
#tolist = ["yuriy@fastzone.ru","tesnus288@gmail.com"]
#msg = '''
#... From:kaze28@yandex.ru
#... Subject: testin ...
#...
#... This is a test'''
#s.sendmail("me@my.org", tolist, msg)
#{"yuriy@fastzone.ru" : (550 ,"User unknown")}
#s.quit()

def test_event (myevent):    
    j = journal.Reader()
    j.this_boot()
    j.log_level(journal.LOG_INFO)
    j.add_match(MESSAGE = myevent)
    for entry in j:                                 
        print(str(entry['__REALTIME_TIMESTAMP'] )+ ' ' + entry['MESSAGE'])

def output_event_in_real_time (massevent):
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
#                    print(str(entry['__REALTIME_TIMESTAMP']) + ' ' + result[0])
                    if (massevent[i]['happened'] + 1) >= (massevent[i]['limit']):
                        print(str(entry['__REALTIME_TIMESTAMP']) + ' ' + result[0])
                        print('Send message administrator')
                        massevent[i]['happened'] == 0
#                        print(result)
                    else:
                        massevent[i]['happened'] += 1
                i += 1


#            print(str(entry['__REALTIME_TIMESTAMP'] )+ ' ' + entry['MESSAGE'])


cfg = yaml.load(open('database.yaml'))

output_event_in_real_time (cfg)