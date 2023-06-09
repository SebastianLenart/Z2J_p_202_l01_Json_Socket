import json
import socket
from user import User


class Client:
    USER = "None"
    HOST = "127.0.0.1"
    PORT = 65432
    MENU = f"""uptime - return timelife of server
info - return version and date of create server
help - return described options, just like that     
stop - stop server and client
login <nick> <password> - let you login to system
logout - let you logout from system
register new user - you can add new user
profil - show info about register user
send message - you can send message to receiver
check all messages
unread messages
list of users
receiver message - you can get message from receiver
Select option: """

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect_ex((self.HOST, self.PORT))
        self.json_to_send = {
            "command": None,
            "user": None,
            "password": None,
            "message": None,
            "is_admin": None
        }
        print(self.MENU)

    def run(self):
        while True:
            command = input(f"you are {self.json_to_send['user']}, please select option: ")
            self.json_to_send["command"] = command
            print(self.json_to_send)
            self.sock.send(json.dumps(self.json_to_send).encode(encoding='utf8'))
            response = self.sock.recv(1024)
            self.response(json.loads(response.decode(encoding="utf8")))

    def response(self, res):
        if "stop" in res["command"].keys():
            print("stop")
            self.sock.close()
            exit()
        if "help" in res["command"].keys():
            print(res["command"]["help"])
            return
        print(res["command"])


if __name__ == '__main__':
    server = Client()
    server.run()
