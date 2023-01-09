import socket
import threading
import json
import pygame, sys, random
from settings import *
import time

HEADER = 10000
PORT = 5050
# SERVER = "192.168.1.63" # private
SERVER = "192.168.1.60" # private
# SERVER = '88.228.26.225' # public
# SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

state = {
	'players':{

	},
	'zombies': {
		'ids': []
	}
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
			# for id, zombie in state['zombies'].items():
			# 	if id != 'ids':
			# 		if zombie['killed']:
			# 			del state['zombies'][id]
			# 			state['zombies']['ids'].remove(id)
			updates = json.loads(msg)
			state['players'][updates['player']['id']] = updates['player']
			if updates['zombies'] != []:
				for zom in updates['zombies']:
					

					if not (zom['id'] in state['zombies']['ids']):
						state['zombies']['ids'].append(int(zom['id']))
						state['zombies'][zom['id']] = zom
					else:
						if not state['zombies'][zom['id']]['killed']:
							state['zombies'][zom['id']] = zom
						else:
							state['zombies'][zom['id']]['killed'] = True

					
					# if zom['killed']:
					# 	del state['zombies'][zom['id']]
					# 	state['zombies']['ids'].remove(zom['id'])
					# 	print(state['zombies'])



			getting = False
			for client in conns:
				client.send( json.dumps(state).encode(FORMAT) )

			print(state)
			# print(f'[{addr}] {msg}')
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