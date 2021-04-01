import socket
import threading
import queue

def RecvData(sock, recvPackets):
    while True:
        data, addr = sock.recvfrom(1024)
        recvPackets.put((data, addr))

host = socket.gethostbyname(socket.gethostname())
port = 5000
print('Server hosting on IP -> ' + str(host))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
clients = set()
recvPackets = queue.Queue()

print('Server Running...')

threading.Thread(target=RecvData, args=(s, recvPackets)).start()

while True:
    while not recvPackets.empty():
        data, addr = recvPackets.get()
        if addr not in clients:
            clients.add(addr)
        clients.add(addr)
        data = data.decode('utf-8')
        if data.endswith('exit'):
            clients.remove(addr)
            continue
        print(str(addr) + data)
        for c in clients:
            if c != addr:
                s.sendto((str(addr[1]) + " " + data).encode('utf-8'), c)
s.close()