import threading
import socket

ip ='127.0.0.1'
port =2500
def sendMessage(socket):
    while True:
        msg = input('')
        socket.sendall(msg.encode(encoding='utf-8'))
        if msg == '/quit':
            print("사용자가 종료를 원합니다.")
            break
def recvMessage(socket):
    while True:
        data = socket.recv(1024)
        msg = data.decode()
        print(msg)
        if msg == '/quit':
            break
    socket.close()
    print('사용자가 퇴장합니다.')

class Client:

    def __init__(self):
        self.clientsock = None

    def socket(self):
        self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsock.connect((ip, port))

    def run(self):
        self.socket()
        t = threading.Thread(target=sendMessage, args=(self.clientsock,))
        t.start()
        t2 = threading.Thread(target=recvMessage, args=(self.clientsock,))
        t2.start()

def main():
    Client().run()

main()
