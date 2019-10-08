import speech_recognition as sr
import socket
import pyttsx as pts
import sys,os,threading,time
print("Execution begin")
api_key1 = "5db169c97645b8c606bcbc686e51fda7"
r=sr.Recognizer()
HOST = '127.0.0.1'
PORT=6373
while 1:
    with sr.Microphone(device_index=1,sample_rate=48000,chunk_size=2048) as source:
        r.adjust_for_ambient_noise(source)
        print("speak something")
        audio=r.listen(source)
        print("<- Listen completed -> ")
        try:
            result = r.recognize_google(audio)
            result = str(result).lower()
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                try:
                    s.connect((HOST,PORT))
                    s.sendall(result.encode())
                    time.sleep(1)
                except (socket.gaierror,ConnectionRefusedError) as e:
                    print("Unable Open the Socket",e.args)
                else:
                    print("The Message is successfully sent")
            print(result)
            result = ""
        except (sr.RequestError,sr.UnknownValueError) as e:
            print("Unable to Recognize The speech",e)
