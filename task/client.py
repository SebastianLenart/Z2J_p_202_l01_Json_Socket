import json
import socket


class Client:
    HOST = "127.0.0.1"
    PORT = 65432
    MENU = """Your options: " 
1.) uptime - return timelife of server 
2.) info - return version and date of create server
3.) help - return described options, just like that            
4.) stop - stop server and client
Select option: """

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect_ex((self.HOST, self.PORT))

    def run(self):
        while True:
            option = input(self.MENU)
            self.sock.send(json.dumps(option).encode(encoding='utf8'))
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
