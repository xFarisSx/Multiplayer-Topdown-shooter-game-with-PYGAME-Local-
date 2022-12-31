import socket
import threading
import json
import pygame, sys, random
from settings import *
import time

HEADER = 1024
PORT = 4040
# SERVER = "192.168.56.1" # private
# SERVER = '88.228.26.225' # public
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

players = {
	'zombies': []
}
conns = []

def handle_client(conn, addr):
	print(f"[NEW CONNECTION] {addr} connected.")

	connected = True
	while connected:
		try:
			msg_length = conn.recv(HEADER).decode(FORMAT)
			if not msg_length: continue
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			if msg == DISCONNECT_MESSAGE:
				connected = False

			player_obj = json.loads(msg)
			players[player_obj['id']] = player_obj
			getting = False
			for client in conns:
				client.send( json.dumps(players).encode(FORMAT) )


			print(f'[{addr}] {msg}')
			# conn.send("Msg received".encode(FORMAT))
		except:
			# print('server error')
			pass
	conn.close()

def start():
	server.listen()
	
	print(f"[LISTENING] server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		conns.append(conn)
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print('[STARTING] server is starting')
start()