import threading
import socket

host = '127.0.0.1'
port = 2500
lock = threading.Lock()

class ChattingRoom:
    def __init__(self):
        self.list = [] #클라이언트 정보를 담을 리스트

    def addUser(self, client):
        self.list.append(client) #클라이언트가 작성한 정보를 토대로 리스트에 클라이언트 추가
        self.sendAll('### 대화 참여자 수 [%d] ###\n'%len(self.list))
        self.sendAll('+++ 채팅 서버 시작+++\n')
        self.sendAll('+++ 종료를 위해 /quit 를 누르세요.+++\n')
        self.sendAll('++ 상대방에 대한 욕설 및 비방은 금지입니다++\n')

    def deleteUser(self, client):
        self.list.remove(client) #클라이언트 정보 삭제

    def sendAll(self, msg): #클라이언트 리스트에 존재하는 클라이언트 모두에게 메세지 전달.
        for conn in self.list:
            conn.sendMessage(msg)
            
class ChatClient:
    def __init__(self, nickname, socket, r):
        self.nickname = nickname
        self.socket = socket
        self.room = r

    def recvMessage(self):
        while True:
            data = self.socket.recv(1024)
            msg = data.decode()
            if msg == '/quit':
                self.sendMessage(msg)
                print(self.nickname,'님이 퇴장했습니다.')
                break

            msg = self.nickname+': ' + msg
            self.room.sendAll(msg)

        self.room.deleteUser(self)
        self.room.sendAll(self.nickname+'님이 퇴장하셨습니다.')


    def sendMessage(self, msg):
        self.socket.sendall(msg.encode(encoding='utf-8'))

    def run(self):
        t = threading.Thread(target=self.recvMessage, args=())
        t.start()

class RunServer:
    def __init__(self):
        self.room = ChattingRoom()
        self.serversock = None

    def ServerOpen(self):
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversock.bind((host,port))
        self.serversock.listen()

    def run(self):
        self.ServerOpen()
        print('+++ 채팅 서버 시작+++')
        print('+++ 종료를 위해 CTRL-C를 누르세요.+++')

        while True:
            client_socket, addr = self.serversock.accept()
            print(addr)
            msg = '사용할 닉네임을 적어주세요!!:'
            client_socket.sendall(msg.encode(encoding='utf-8'))
            msg = client_socket.recv(1024)
            nickname = msg.decode()
            chatclient = ChatClient(nickname, client_socket, self.room)
            self.room.addUser(chatclient)
            chatclient.run()

            #print('+++채팅방 참여자 수 [%d]' %len(ChattingRoom.addUser().self.list))
            #print(self.nickname,'님이 채팅방에 참여했습니다.')

def main():
    RunServer().run()

main()


                                                                                                                                                    89        89,0-1        Bot
