import socket
import datetime
from src.net.user import User
from threading import Lock
from random import randint
from src.data.data import get_time_now, get_difference_time
from src.data.userdatabase import ListUser
def get_time_now():
    dt = datetime.datetime.now()
    return (dt - datetime.datetime(dt.year, dt.month, dt.day)).total_seconds()
def get_difference_time(first_time, second_time):
    return first_time - second_time#.total_seconds()

class HandlePlayers:
    def __init__(self, server_socket, udb):
        self.server_socket = server_socket
        self.locker = Lock()
        self.list_user = ListUser()
        self.user_data_base = udb
        self.count_connect = 0
        self.time_difference_connect = get_time_now()
        self.is_stop_handle_connect = False
        self.time_stop_handle_connect = 0

        self.list_user.start()

    def run(self):
        if self.is_stop_handle_connect:
            stop_difference = get_difference_time(get_time_now(), self.time_stop_handle_connect)
            #print(f"STOP DIFFERENCE TIME:{stop_difference}, need 5 TIMES")
            if stop_difference >= 5:
                self.is_stop_handle_connect = False
                self.time_difference_connect = 0
            else:
                return

        client_socket, client_address = self.server_socket.accept()

        # CHECK DDOS
        time_difference = get_difference_time(get_time_now(), self.time_difference_connect)
        self.time_difference_connect = get_time_now()
        if time_difference <= 3:
            self.count_connect += 1
        else:
            self.count_connect = 0
        if self.count_connect == 6:
            #Sprint("DDOS ATTACK DETECTED")
            self.count_connect = 0
            self.is_stop_handle_connect = True
            client_socket.send('{"response":"kick", "text":"You are kicked\nYou connected to the server, but you were kicked because there was a DDOS attack on the server. If you are not a participant in the DDOS attack, then please wait. If the server still won΄t let you in because of this reason, then contact the administrator."}'.encode())
            client_socket.close()
            return

        # CHECK IS BANNED
        player = User(self.locker,self.server_socket, client_socket, self.user_data_base)
        player.start()
        # get name
        id_player = str(get_time_now()) + " - " + str(randint(0, 99999))
        player.username = id_player
        self.list_user.append(id_player, player)
