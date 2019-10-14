import os,sys,time
from multiprocessing import Process
def startElsaRecoganize():
    os.system("python3 /home/pi/git/project/Project/src/libs/speech/ElsaSpeechRecognizer.py")
def startElsaSpeek():
    os.system("python3 /home/pi/git/project/Project/src/libs/speech/ElsaSpeechSynthesizer.py")
def startTelegram():
    os.system("python3 /home/pi/git/project/Project/src/telegrambot.py")
def startBrain():
    os.system("python3 /home/pi/git/project/Project/src/Brain.py")
p1= Process(target=startBrain,args=())
p2= Process(target=startElsaSpeek,args=())
p3= Process(target=startTelegram,args=())
p4= Process(target=startElsaRecoganize,args=())

print("BOOTING",end='')
time.sleep(2)
for i in range(5):
    print('.',end='')
    time.sleep(1)
print('\n')

p1.start()
print('Brain Initalizing...')
time.sleep(2)
p2.start()
print('Starting Speech Sythesis Engine...')
time.sleep(2)
p3.start()
print('Starting Telegramservices...')
time.sleep(1)
p4.start()
print('Starting Speech Recoganizing Engine...')
p1.join()
p2.join()
p3.join()
p4.join()
    
