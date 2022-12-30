import socket
import threading
import json
import pygame, sys, random
from settings import *
import time

HEADER = 1024
PORT = 5050
# SERVER = "192.168.56.1" # private
# SERVER = '88.228.26.225' # public
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

players = {
	
}


def handle_client(conn, addr):
	print(f"[NEW CONNECTION] {addr} connected.")
	setting = False
	getting = False

	connected = True
	while connected:
		try:
			msg_length = conn.recv(HEADER).decode(FORMAT)
			if not msg_length: continue
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			if msg == DISCONNECT_MESSAGE:
				connected = False
			# if msg == 'setting':
			# 	print('setted')
			# 	msg_length = conn.recv(HEADER).decode(FORMAT)
			# 	print('setted2')
			# 	if not msg_length: continue
			# 	msg_length = int(msg_length)
			# 	msg = conn.recv(msg_length).decode(FORMAT)
			# 	player_obj = json.loads(msg)
			# 	players[player_obj['id']] = player_obj
			# 	print(players)

			if setting:
				player_obj = json.loads(msg)
				players[player_obj['id']] = player_obj
				getting = False

			if getting:
				value = ''
				other = ''
				id = msg
				if players == {}:
					continue
				for key in players:
					if str(key) != str(id):
						value = players[key]
						other = value 
				if other and other != '':
					conn.send(json.dumps(other).encode(FORMAT))
					print('here')
				setting = False
				getting = False
				

			if msg == 'setting':
				setting = True
			else:
				setting = False

			if msg == 'getting':
				getting = True
			else: 
				getting = False


			print(f'[{addr}] {msg}')
			conn.send("Msg received".encode(FORMAT))
		except:
			print('server error')
	conn.close()

def start():
	server.listen()
	print(f"[LISTENING] server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print('[STARTING] server is starting')
start()