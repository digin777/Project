import threading
#from src.Alaram import alarm
import pyttsx3 as pts
import sys
sys.path.append("E:\\DIJIN\\jetbrains\\Python\\project1\\src\\libs")
import socket
from libs.weather.Weather import *


elsa=pts.init()
connectives=['in', 'at', 'is','a','an','and','the','are','with','for','on']
days=['today','yesterday','tomorrow',"yesterday's","today's","tomarrows","tomorrow's"]
qust=['what','where','when','why','who','how','whats',"hows","how's","whos","what's","where's","wheres","whys","why's","who's"]
info=['my','you','your','i','you’s','mine','yours',]
commamds=['alarm','timer','remind','weather','score','recipe','bible','nearby','reminder','trun','switch']
HOST = '127.0.0.1'
PORT=6373

class Parser():
    def __init__(self):
        self.x=0
    def wearher_checking(self,inp_arry):
        stripped_array=inp_arry[inp_arry.index('weather')+1:]
        print("weather")
        for conective in connectives:
            if conective in stripped_array:
                stripped_array.remove(conective)
        weather_detials=getwether(stripped_array.pop())
        print(weather_detials)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, 6687))
                s.sendall(weather_detials.encode())
            except (socket.gaierror, ConnectionRefusedError) as e:
                print("Unable Open the Socket")
            else:
                print("The Message is successfully sent")

    def alaram(self,inp_arry):
        stripped_array=inp_arry[inp_arry.index('alarm')+1:]
        a_hour=a_minute=None
        for conective in connectives:
            if conective in stripped_array:
                stripped_array.remove(conective)
        if len(stripped_array)==0:
            print("Canot set an alaram")
        elif len(stripped_array)==1:
            if stripped_array[0].isdigit():
                a_hour=stripped_array[0]
                a_minute=0
            elif len(stripped_array[0].split(':'))!=0:
                a_hour=stripped_array[0].split(':')[0]
                a_minute=stripped_array[0].split(':')[1]
        elif len(stripped_array)==2:
            if stripped_array[0].isdigit():
                a_hour=stripped_array[0]
                a_minute=0
            elif len(stripped_array[0].split(':'))!=0:
                a_hour=stripped_array[0].split(':')[0]
                a_minute=stripped_array[0].split(':')[1]
            if stripped_array[1]=='p.m.':
                a_hour=int(a_hour)
                if a_hour<12:
                    a_hour+=12
        if a_hour and a_minute is not None:
            a_hour,a_minute=int(a_hour),int(a_minute)
            if a_hour>24 or a_minute>59:
                print("Please Provide valid Time")
            else:
                pass
                #alarm.setalaram(int(a_hour),int(a_minute))
    def IoT(self,inp_arry,command):
        stripped_array=inp_arry[inp_arry.index(command)+1:]
        print(stripped_array)
        for connective in connectives:
            if connective in stripped_array:
                while stripped_array.count(connective)>0:
                    stripped_array.remove(connective)
        print(stripped_array)
    def getInfo(self,inp):
        inp=str(inp).lower()
        inp_arry=inp.split(' ')
        print(inp_arry)
        main_list=[commamds,qust,info,days,connectives]
        par_dict={}
        for item in main_list:
            out_arr=[]
            for i in item:
                if i in inp_arry:
                    out_arr.append(i)
            key=''
            if item==commamds:
                key='commands'
            elif item==days:
                key='days'
            elif item==qust:
                key='quest'
            elif item==info:
                key='info'
            elif item==connectives:
                key='connectives'
            par_dict[key]= out_arr
        self.par_dict = par_dict
        for command in commamds:
            if command in inp:
                if command is 'weather':
                    self.wearher_checking(inp_arry)
                elif command is 'alarm':
                    self.alaram(inp_arry)
                elif command is 'switch' or command is 'turn':
                    self.IoT(inp_arry,command)
try:
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        while 1:
            s.listen()
            conn,addr=s.accept()
            print("Connected to ",addr)
            while 1:
                data = conn.recv(1024).decode()
                if not data:
                    break
                parser = Parser()
                threading.Thread(target=parser.getInfo, args=(data,), daemon=True).start()
except Exception as e:
    print("Output is Not allowed",e.args)