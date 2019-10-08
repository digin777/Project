from multiprocessing import Process
import os
import sys
sys.path.append("home/pi/git/project/Project/src/libs")
def sub1():
	os.system(" python3 /home/pi/git/project/Project/src/libs/speech/ElsaSpeechRecognizer.py")
def sub2():
	os.system(" python3 /home/pi/git/project/Project/src/libs/speech/ElsaSpeechSynthesizer.py")
def sub3():
	os.system(" python3 /home/pi/git/project/Project/src/libs/Brain.py")
def startprocess():
	x=Process(target=sub1)
	y=Process(target=sub2)
	z=Process(target=sub3)
	x.start()
	y.start()
	z.start()
	x.join()
	y.join()
	z.join()
if __name__=='__main__':
	startprocess()
