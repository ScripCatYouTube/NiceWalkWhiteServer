import json
import socket

from threading import Thread, Lock
from src.data.data import is_in
from src.data.userdatabase import UserDatabase
from src.data.types import check_of_type

class User(Thread):
    def __init__(self, locker: Lock,server: socket.socket , client: socket.socket, db: UserDatabase):
        super().__init__()
        self.server = server
        self.client = client
        self.username = None
        self.password = None
        self.db = db
        self.is_delete = False
        self.reg_data = {"is_register":True}
        self.locker = locker
    def run(self):
        while True:
            if self.is_delete: break
            try:
                data = self.client.recv(1024)
                if data:
                    self.handle_get(data)
            except Exception as e:
                print(e)
                self.kick("Reason: bad getted packet")
    def kick(self, msg = ""):
        try:
            text = "You are kicked"
            if msg != "":
                text += "\n" + msg
            self.send({"response":"kick", "text":text})
            self.client.close()
            #print("Kicked,", self.username)
            self.is_delete = True
        except Exception as e:
            self.is_delete = True
    def handle_get(self, _data):
        data = _data.decode("utf-8")
        try:
            json_data = json.loads(data)
            if is_in(json_data, "response"):
                self.parse_json_data(json_data)
        except json.decoder.JSONDecodeError as e:
            self.kick("Reason: bad json, json:",data)

    def parse_json_data(self, json_data):
        if json_data["response"] == "register":
            if self.password == None or self.name == None:
                if is_in(json_data, "content"):
                    if is_in(json_data["content"], "password") and is_in(json_data["content"], "name") and is_in(json_data["content"], "token"):
                        print(f"LOGIN, data:{json_data}")
                        if self.db.check_account(json_data["content"]["name"], json_data["content"]["password"], json_data["content"]["token"]):
                            self.username = json_data["content"]["name"]
                            self.password = json_data["content"]["password"]
                            return
                        else:
                            self.kick("Reason: not found account")
                            return
                    elif is_in(json_data["content"], "password") and is_in(json_data["content"], "name"):
                        if self.db.check_username(json_data["content"]["name"]):
                            self.kick("Reason: you are trying to register with an existing nickname")
                            return
                        name = json_data["content"]["name"]
                        password = json_data["content"]["password"]
                        if check_of_type(str, name, password):
                            __token = self.db.generator_token(15)
                            self.db.register(name, password, __token)
                            print(f"REGISTER, data:{json_data}, Registred user: {name}:{password} token:{__token}")
                        else:
                            self.kick("Reason: your name or password types is not string")
                        
    def send(self, json_data):
        try:
            self.client.send(str(json_data).replace("'",'"').encode("utf-8"))
            return True
        except Exception as e:
            return e



