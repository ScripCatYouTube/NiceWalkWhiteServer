import socket

from src.data.userdatabase import UserDatabase
from src.net.net import HandlePlayers

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_host = '127.0.0.1'
server_port = 7556
server_players = 32
server_socket.bind((server_host, server_port))

server_socket.listen(server_players)
userdb = UserDatabase("users", path = 'luggage/users')

players = HandlePlayers(server_socket, userdb)

print(f"Server listen on {server_host}:{server_port}, max players {server_players}")

while True:
    while True:
        players.run()
