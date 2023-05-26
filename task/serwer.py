import json
import datetime
import socket


class Serwer:
    HOST = "127.0.0.1"
    PORT = 65432
    HELP = """uptime - return timelife of server
info - return version and date of create server
help - return described options, just like that     
stop - stop server and client"""

    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.date_of_create = self.start_time.strftime("%d/%m/%Y")
        print(self.date_of_create)
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.HOST, self.PORT))
        self.lsock.listen()
        print(f"Listening on {(self.HOST, self.PORT)}")
        self.stop = False

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
                if self.stop:
                    break

    def options(self, data, conn):
        answer_to_send = {"command": {"bład": "Nie rozpoznano polecenia"}}
        if data == "uptime":
            answer = {"uptime": str(datetime.datetime.now() - self.start_time)[:7]}
            answer_to_send["command"] = answer
            print(answer_to_send["command"])
        if data == "info":
            answer = {"info:": f"Version: {'1.0.0'}, date of create server: {self.date_of_create}"}
            answer_to_send["command"] = answer
            print(answer_to_send["command"])
        if data == "help":
            answer = {"help": self.HELP}
            answer_to_send["command"] = answer
            print(answer_to_send["command"])
        if data == "stop":
            answer = {"stop": "stop"}
            answer_to_send["command"] = answer
            self.stop = True
            print(answer_to_send["command"])

        answer_to_send = json.dumps(answer_to_send).encode(encoding='utf8')
        conn.sendall(answer_to_send)

        if self.stop:
            self.lsock.close()


if __name__ == '__main__':
    server = Serwer()
    server.run()
