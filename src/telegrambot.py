#coder :- DIJIN ANTONY

import sys
import time,socket,threading
import random
import datetime
import telepot
sys.path.append("/home/pi/git/project/Project/src/")
from libs.IoT import IOT
global s_msg,status
s_msg=0
status={'lbed':'OFF','fbed':'OFF','lmain':'OFF','fmain':'OFF'}
HOST = '127.0.0.1'
PORT=6373
def on(pin):
       IOT.performIOT(pin,'ON')
       return 'ON'
def off(pin):
        IOT.performIOT(pin,'OFF')
        return 'OFF'
def passmessage(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, 6687))
                s.sendall(("an Message is Recived \n"+message).encode())
            except (socket.gaierror, ConnectionRefusedError) as e:
                print("Unable Open the Socket")
            else:
                print("The Message is successfully sent")

def handle(msg):
    global s_msg,status
    chat_id = msg['chat']['id']
    command = msg['text']
    port_map={'lbed':10,'fbed':12,'lmain':16,'fmain':18}
    
    print ('Got command: %s' % command,chat_id)
    if 'lbedon' in command.lower() :
       bot.sendMessage(chat_id, on(10))
       status['lbed']='ON'
    elif 'lbedoff' in command.lower():
        bot.sendMessage(chat_id, off(10))
        status['lbed']='OFF'
    elif 'fbedon' in command.lower():
        bot.sendMessage(chat_id, on(12))
        status['fbed']='ON'
    elif 'fbedoff' in command.lower():
        bot.sendMessage(chat_id, off(12))
        status['fbed']='OFF'
    elif 'lmainon' in command.lower():
       bot.sendMessage(chat_id, on(16))
       status['lmain']='ON'
    elif 'lmainoff' in command.lower():
       bot.sendMessage(chat_id, off(16))
       status['lmain']='OFF'
    elif 'fmainon' in command.lower():
        bot.sendMessage(chat_id, on(18))
        status['fmain']='ON'
    elif 'fmainoff' in command.lower():
        bot.sendMessage(chat_id, off(18))
        status['fmain']='OFF'
    elif command.lower() == '/start':
        bot.sendMessage(chat_id,"Welcome to ELSA")
    elif command.lower() == '/message':
        bot.sendMessage(chat_id,"Send Message")
        s_msg=int(msg['message_id'])
    elif int(msg['message_id'])==s_msg+2:
        message=command.lower()
        bot.sendMessage(chat_id,"Message is Recived")
        threading.Thread(target=passmessage,args=(message,)).start()
    elif command.lower()=='/status':
        ret_str=''
        for i,v in status.items():
            ret_str+=i+':'+v+'\n'
        bot.sendMessage(chat_id,ret_str)
        


bot = telepot.Bot('-api key-')
bot.message_loop(handle)
print ('I am listening...')

while 1:
     time.sleep(10)
