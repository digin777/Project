HOST = '127.0.0.1'
PORT=6373
import socket,time
def Msgpass(string):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, 6687))
                s.sendall(string.encode())
            except (socket.gaierror, ConnectionRefusedError) as e:
                print("Unable Open the Socket")
            else:
                print("The Message is successfully sent")

