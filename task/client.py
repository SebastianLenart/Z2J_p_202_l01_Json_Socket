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
logout <nick> - let you logout from system
register <nick> <password> <admin>- only admin can add new user
info_user <nick> - only admin can see info about everybody
send <nick> <message> - only register user can send message to receiver
show_conversation <nick> - only login user see conversation
show_unread_texts - only login user see unread texts
list_of_users - only login user can see list of users
Select option: """

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect_ex((self.HOST, self.PORT))
        self.command = None
        self.get_json = {"answer": "Nie rozpoznano polecenia",
                         "nick": "default",
                         "password": "",
                         "admin": "default",
                         "messages": ""}
        print(self.MENU)

    def run(self):
        while True:
            command = input(f"You are {self.get_json['nick']} ({self.get_json['admin']}), please select option: ")
            self.command = command.split(" ")
            self.sock.send(json.dumps(self.command).encode(encoding='utf8'))
            json_from_server = self.sock.recv(1024)
            self.response(json.loads(json_from_server.decode(encoding="utf8")))

    def response(self, res):
        commands = ["uptime", "info", "help"]
        if "stop" in res["command"]:
            print("stop")
            self.sock.close()
            exit()
        elif any(res["command"] in command for command in commands):
            print(res["answer"])
            return
        elif "login" in res["command"]:
            self.get_json[]



if __name__ == '__main__':
    client = Client()
    client.run()
