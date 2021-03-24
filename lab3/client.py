import socket
import threading
import random
import os
import hashlib
import pickle


def ReceiveData(sock):
    global srv_msg
    while True:
        try:

            data, addr = sock.recvfrom(1024)
            srv_msg += 'Receiving data from the server...\n'
            print(read_data(data))
        except ConnectionResetError as c:
            ReceiveData(sock)

HEADERSIZE = 10

def change_msg(msg):
    msg = pickle.dumps(msg)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
    return msg

def read_data(msg):
    return pickle.loads(msg[HEADERSIZE:])

host = socket.gethostbyname(socket.gethostname())

srv_msg = ''

k = 0
while k < 2:
    try:
        k += 1
        port = int(input("Enter the port number between 3000 and 10000.\n"))
        print("You entered the port: " + str(port))
        break
    except (ValueError, OSError):
        print("Error! The port is already used or incorrectly specified.")
        if k == 2:
            port = random.randint(3000, 10000)
            print("Your default port: ", port)
        else:
            continue

print('Client IP -> ' + str(host))
print('Port -> ' + str(port))

with open("users.txt", 'r') as file:
    lines = file.read().splitlines()

while True:
    k = 0

    users = dict()
    for line in lines:
        user = line.split("; ")
        users[user[0]] = [user[1], user[2]]

    while k < 2:
        k += 1
        try:
            serverIP = str(input('Enter Server IP: '))
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if serverIP == "exit":
                s.close()
                os._exit(0)
                break
            serverPort = int(input('Enter Server Port: '))
            server = (serverIP, serverPort)
            s.bind((host, port))
            s.connect((server)) # just for exception
            break
        except (ValueError, OSError):
            print('Invalid Server IP or Server Port! Please try again. ')
            if k == 2:
                serverIP = '192.168.56.1'
                serverPort = 5000
                server = (serverIP, serverPort)
                print('Default host: ', serverIP)
                print('Default port: ', serverPort)
            else:
                continue

    srv_msg += 'Connected to the server...\n'

    if host in users:
        print('Welcome, ' + users[host][0] + '!')
        name = users[host][0]
        password = users[host][1]
        k = 0
        while k < 3:
            k += 1
            check_password = str(input('Please enter your password: '))
            check_password = hashlib.md5(check_password.encode())
            if str(check_password.hexdigest()) == password:
                print('The password is correct.')
                break
            else:
                print('The password is incorrect.')
                if k == 3:
                    print('Access is blocked.')
                    os._exit(0)
                continue
    else:
        name = input('Please write your name here: ')
        if name == '':
            name = 'Guest' + str(random.randint(1000, 9999))
            print('Your name is:' + name)

        password = str(input('Please enter your new password: '))
        password = hashlib.md5(password.encode())
        with open('users.txt', 'a') as file:
            file.write(host + '; ' + name + '; ' + str(password.hexdigest()) + '\n')

    s.sendto(change_msg(name), server)
    threading.Thread(target=ReceiveData, args=(s,)).start()
    while True:
        print("Enter your message: ")
        data = input()
        if data == 'exit':
            s.close()

            srv_msg += 'Disconnecting the server connection...\n'

            logs_file = open('ClientServer.log', 'a')
            logs_file.write(srv_msg)
            logs_file.close()

            os._exit(0)
            break
        elif data == '':
            continue
        data = change_msg( '[' + name + '] -> ' + data)
        s.sendto(data, server)
        srv_msg += 'Sending data to the server...\n'
    s.sendto(data.encode('utf-8'), server)

s.close()
