import time,sys
sys.path.append("/home/pi/git/project/Project/src/")
import datetime as dt
from threading import Thread
from libs.MsgPass.msgpass import *
import pygame

global count,rcount


def newalaram(tme, count):
    while 1:
        current = str(dt.datetime.now().time())
        current = current[:5]
        if current == tme:
            Msgpass("wake up sir you have an alarm")
            print("Alarm - " + str(count) + " stoped")

            time.sleep(2)
            file = '/home/pi/git/project/Project/src/res/cool_alarm_music.mp3'
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            break


def setalaram(h, m):
    count = 0
    tme = str(dt.time(h, m, 0))
    tme = tme[:5]
    try:
        count += 1
        t = Thread(target=newalaram, args=(tme, count,), daemon=True)
        t.start()
        time.sleep(5)
        Msgpass(f"got it your Alarm  setted at {h} {m}")
    except Exception as e:
        Msgpass(" Unable to set Alarm", e.args)

def newreminder(tme,msg):
    while 1:
        current = str(dt.datetime.now().time())
        current = current[:5]
        if current == tme:
            Msgpass(f"You have an reminder about {msg}")
            print("reminder is" + " stoped")
            break


def setreminder(h,m,msg):
    #rcount = 0
    tme = str(dt.time(h, m, 0))
    tme = tme[:5]
    try:
        #count += 1
        t = Thread(target=newreminder, args=(tme, msg,), daemon=True)
        t.start()
        time.sleep(5)
        Msgpass(f"got it I will remind you about {msg} at {h} {m}")
    except Exception as e:
        Msgpass(" Unable to set reminder"+ str(e.args))
def main():
    setreminder(13,46,'Hellow world')

if __name__ == '__main__':
    main()
