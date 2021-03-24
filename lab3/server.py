import socket
import threading
import queue
import random
import pickle

def RecvData(sock,recvPackets):
    global srv_msg, users
    while True:
        try:
            srv_msg += 'Connected to the client...\n'
            data,addr = sock.recvfrom(1024)
            srv_msg += 'Receiving data from the client...\n'
            recvPackets.put((data,addr))
        except ConnectionResetError:
            RecvData(sock, recvPackets)

HEADERSIZE = 10

def change_msg(msg):
    msg = pickle.dumps(msg)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
    return msg

def read_data(msg):
    return pickle.loads(msg[HEADERSIZE:])

host = socket.gethostbyname(socket.gethostname())

srv_msg = "" # для служебных сообщений
print('Server hosting on IP-> '+str(host))
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

k = 0
while k < 2:
    try:
        k += 1
        port = int(input("Enter the port number between 3000 and 10000.\n"))
        print("You entered the port: " + str(port))
        s.bind((host, port))
        break
    except (ValueError, OSError):
        print("Error! The port is already used or incorrectly specified.")
        if k == 2:
            port = random.randint(3000, 10000)
            s.bind((host, port))
            print("Your default port: ", port)
        else:
            continue

srv_msg += 'Start listening to the port...\n'

clients = set()

recvPackets = queue.Queue()

print('Server Running...')

threading.Thread(target=RecvData,args=(s,recvPackets)).start()

while True:

    while not recvPackets.empty():
        data,addr = recvPackets.get()
        if addr not in clients:
            clients.add(addr)
            continue
        clients.add(addr)
        data = read_data(data)
        if data.endswith('exit'):
            clients.remove(addr)
            continue
        print(str(addr)+ data)
        for c in clients:
            if c!=addr:
                s.sendto(change_msg(data),c)
                srv_msg += 'Sending data to the client...\n'
            else:
                s.sendto(change_msg('just for the test'), c)

        srv_msg += 'Disabling the client...\n'
        srv_msg += 'Stopping the server...\n'
        logs_file = open('ClientServer.log', 'a')
        logs_file.write(srv_msg)
        logs_file.close()
s.close()

