import random
import sqlite3

from threading import Thread
from data import get_int_time, enscrypt_sha256

class UserDatabase:
    def __init__(self,name,path = "luggage/users"):
        self.db = sqlite3.connect(path + ".db", check_same_thread=False)
        self.name = name
        self.space_token = " "
        self.seed = str(get_int_time())
        self.init_table()

    def execute(self, command):
        cursor = self.db.cursor()
        cursor.execute(command)
        self.db.commit()
        return cursor

    def init_table(self):
        self.execute(f""" CREATE TABLE IF NOT EXISTS {self.name}(name TEXT, password TEXT, tokens TEXT); """)

    def register(self, name, password, tokens = ""):
        _is_account = self.check_account(name, password)
        if _is_account == False:
            self.add_data(name, password, tokens)
            return True
        else:
            return False

    def add_data(self, name, password, tokens):
        self.execute(f""" INSERT INTO {self.name}(name, password, tokens) VALUES('{name}', '{password}', '{tokens}');""")

    def check_account(self, name, password):
        for i in self.get_data():
            if i[0] == name and i[1] == password:
                return True
        return False

    def check_username(self, name):
        for i in self.get_data():
            if i[0] == name:
                return True
        return False

    def get_data(self):
        _data_res = []
        for i in self.execute(f""" SELECT name, password, tokens FROM {self.name};"""):
            _data_res.append(i)
        return _data_res
    def get_accounts_data_name(self, name):
        for i in self.get_data():
            if i[0] == name:
                return True
        return False
    def delete_data_name(self, name):
        self.execute(f"""DELETE FROM  {self.name} WHERE name = '{name}'""")

    def delete_data_password(self, password):
        self.execute(f"""DELETE FROM  {self.name} WHERE password = {password}""")

    def change_account(self, name, password, tokens):
        self.delete_data_name(name)
        self.add_data(name, password, tokens)

    def clear_all(self):
        for i in self.get_data():
            self.delete_data_name(i[0])

    def get_data_account(self, name):
        for i in self.get_data():
            if i[0] == name:
                return i
        return False

    def is_account_name_password(self, name, password):
        for i in self.get_data():
            if i[0] == name and i[1] == password:
                return True
        return False

    def generator_token(self, len_token = 15):
        token = ""
        alphabet = "1234567890_=+-()*&$%!@#qwertyuiopasdfghjkl{}zxcvbnm<>.,"
        random.seed = get_int_time()
        for i in range(len_token+1):
            token += alphabet[random.randint(0,len(alphabet)-1)]
        return enscrypt_sha256(token + str(get_int_time()) + str(random.randint(-9999,9999)))

    def save_tokens(self, name, tokens = []):
        data_account = self.get_accounts_data_name(name)
        if data_account:
            text = ""
            for index, i in enumerate(tokens):
                if len(tokens) == index + 1:
                    text += i
                elif len(tokens) >= index + 1:
                    text += i + self.space_token
            print(text)
            data_about_username = self.get_data_account(name)
            self.change_account(name, data_about_username[1], text)
            return True
        return False

    def get_tokens(self, name):
        data_account = self.get_accounts_data_name(name)
        if data_account:
            data = self.get_data_account(name)
            return data[2].split(" ")
        return False

    def is_token(self, name, token):
        data = self.get_tokens(name)
        if data == False:
            return False
        if token in data:
            return True
        else:
            return False

class ListUser(Thread):
    def __init__(self):
        self.list_users = {}
        super().__init__()
    def append(self, name, user_class):
        self.list_users[name] = user_class
    def delete(self):
        try:
            for i in self.list_users:
                if self.list_users[i].is_delete:
                    self.list_users[i].client.close()
                    del self.list_users[i]
        except RuntimeError as e:
            pass
    def run(self):
        while True:
            self.delete()
    def get(self):
        return self.list_users