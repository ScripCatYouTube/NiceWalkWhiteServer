import socket

class Connecter:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self, address, port):
        self.sock.connect((address, port))
    def send(self, msg: str):
        self.sock.send(msg.replace("'",'"').encode("utf-8"))
    def get(self):
        return self.sock.recv(1024).decode("utf-8")
    def close(self):
        self.sock.close()


if __name__ == "__main__":
    for i in range(10000):
        con = Connecter()
        con.connect("127.0.0.1", 7556)
        con.close()
        #con.send(str({"response":"register", "content":{"name":"U", "password":"top"}}))

