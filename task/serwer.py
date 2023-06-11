import json
import datetime
import socket
from user import User

class Serwer:
    HOST = "127.0.0.1"
    PORT = 65432
    HELP = """uptime - return timelife of server
info - return version and date of create server
help - return described options, just like that     
stop - stop server and client
login - let you login to system
logout - let you logout from system
register new user - you can add new user
profil - show info about register user
send message - you can send message to receiver
receiver message - you can get message from receiver"""

    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.date_of_create = self.start_time.strftime("%d/%m/%Y")
        print(self.date_of_create)
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.HOST, self.PORT))
        self.lsock.listen()
        print(f"Listening on {(self.HOST, self.PORT)}")
        self.stop = False
        self.answer_to_send = {"command": {"bład": "Nie rozpoznano polecenia"}}
        self.user = User()

    def run(self):
        conn, addr = self.lsock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")

        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                print("data1: ", data)
                sdata = json.loads(data.decode(encoding="utf8"))
                if not sdata:
                    break
                self.options(sdata, conn)
                if self.stop:
                    break

    def options(self, data, conn):
        print("data2: ", data)
        if data == "uptime":
            self.uptime()
        if data == "info":
            self.info()
        if data == "help":
            self.help()
        if data == "stop":
            self.stop()

        self.answer_to_send = json.dumps(self.answer_to_send).encode(encoding='utf8')
        conn.sendall(self.answer_to_send)

        if self.stop:
            self.lsock.close()

    def uptime(self):
        answer = {"uptime": str(datetime.datetime.now() - self.start_time)[:7]}
        self.answer_to_send["command"] = answer
        print(self.answer_to_send["command"])

    def info(self):
        answer = {"info:": f"Version: {'1.0.0'}, date of create server: {self.date_of_create}"}
        self.answer_to_send["command"] = answer
        print(self.answer_to_send["command"])

    def help(self):
        answer = {"help": self.HELP}
        self.answer_to_send["command"] = answer
        print(self.answer_to_send["command"])

    def stop(self):
        answer = {"stop": "stop"}
        self.answer_to_send["command"] = answer
        self.stop = True
        print(self.answer_to_send["command"])


if __name__ == '__main__':
    server = Serwer()
    server.run()
