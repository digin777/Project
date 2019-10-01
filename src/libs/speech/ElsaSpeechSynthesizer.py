import pyttsx3 as pts
import socket
elsa=pts.init()
elsa.setProperty('rate',150)
HOST = '127.0.0.1'
PORT=6687
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
                elsa.say(data),elsa.runAndWait()
                print(data)
except Exception as e:
    print("Output is Not allowed",e.args)