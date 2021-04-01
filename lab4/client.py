import socket
import threading
import random
import os

def ReceiveData(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(data.decode('utf-8'))
        except:
            pass

host = socket.gethostbyname(socket.gethostname())
port = random.randint(6000, 10000)
print('Client IP -> ' + str(host))
print('Port -> ' + str(port))

while True:

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ("192.168.56.1", 5000)
    s.bind((host, port))

    threading.Thread(target=ReceiveData, args=(s,)).start()
    while True:
        print("Enter your message: ")
        data = input()
        if data == 'exit':
            s.close()
            os._exit(0)
            break
        elif data == '':
            continue
        data = '-> ' + data
        s.sendto(data.encode('utf-8'), server)
    s.sendto(data.encode('utf-8'), server)

s.close()