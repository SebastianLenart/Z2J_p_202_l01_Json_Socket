import json
import datetime
import socket
from user import User


class Serwer:
    HOST = "127.0.0.1"
    PORT = 65432
    HELP = f"""uptime - return timelife of server
info - return version and date of create server
help - return described options, just like that     
stop - stop server and client
login <nick> <password> - let you login to system
logout <nick> - let you logout from system
register <nick> <password> <admin>- only admin can add new user
info_user <nick> - only admin can see info about everybody
send <nick> <message> - only register user can send message to receiver
show_conversation <nick> - only login user see conversation
show_unread_texts - only login user see unread texts
list of users - only login user can see list of users
"""

    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.date_of_create = self.start_time.strftime("%d/%m/%Y")
        print(self.date_of_create)
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.HOST, self.PORT))
        self.lsock.listen()
        print(f"Listening on {(self.HOST, self.PORT)}")
        self.stopFlag = False
        self.answer_to_send = {"command": "Nie rozpoznano polecenia",
                               "answer": "",
                               "nick": "",
                               "password": "",
                               "admin": "",
                               "messages": ""}
        self.user = User()

    def run(self):
        conn, addr = self.lsock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")

        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                sdata = json.loads(data.decode(encoding="utf8"))
                if not sdata:
                    break
                self.options(sdata, conn)
                if self.stopFlag:
                    break

    def options(self, data, conn):
        if data[0] == "uptime":
            self.uptime()
        elif data[0] == "info":
            self.info()
        elif data[0] == "help":
            self.help()
        elif data[0] == "stop":
            self.stop()
        elif data[0] == "login":
            self.login(data)

        self.answer_to_send = json.dumps(self.answer_to_send).encode(encoding='utf8')
        conn.sendall(self.answer_to_send)
        self.default_answer()

        if self.stopFlag:
            self.lsock.close()

    def default_answer(self):
        self.answer_to_send = {"command": "Nie rozpoznano polecenia",
                               "answer": "",
                               "nick": "",
                               "password": "",
                               "admin": "",
                               "messages": ""}

    def uptime(self):
        answer = str(datetime.datetime.now() - self.start_time)[:7]
        self.answer_to_send["command"] = "uptime"
        self.answer_to_send["answer"] = answer
        print(self.answer_to_send["answer"])

    def info(self):
        answer = f"Version: {'1.0.0'}, date of create server: {self.date_of_create}"
        self.answer_to_send["command"] = "info"
        self.answer_to_send["answer"] = answer
        print(self.answer_to_send["answer"])

    def help(self):
        answer = self.HELP
        self.answer_to_send["command"] = "help"
        self.answer_to_send["answer"] = answer
        print(self.answer_to_send["answer"])

    def stop(self):
        answer = "stop"
        self.answer_to_send["command"] = "stop"
        self.answer_to_send["answer"] = answer
        self.stopFlag = True
        print(self.answer_to_send["answer"])

    def login(self, data: dict):
        self.answer_to_send["command"] = "login"
        self.answer_to_send["answer"] = self.user.login(data[1], data[2])
        self.answer_to_send["nick"] = self.user.nick
        # self.answer_to_send["password"] = self.user.password
        self.answer_to_send["admin"] = self.user.nick
        print(self.answer_to_send["answer"])

if __name__ == '__main__':
    server = Serwer()
    server.run()
