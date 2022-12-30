import pygame, sys, random, json
from settings import *
from level import Level
from ui import UI

import socket
import time
class Network:
    def __init__(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.recieves = []
        self.last_recieve = ''
        self.player = ''
        self.other = ''

    def recieve(self, msg):
        self.recieves.append(msg)
        self.last_recieve = self.recieves[-1]
        if not self.last_recieve:
            return 
        if self.last_recieve == '' or self.last_recieve == ' ':
            return
        if self.last_recieve.startswith("{"):

            self.others = json.loads(self.last_recieve)
            for _,value in self.others.items():
                if value['id'] != self.player['id']:
                    self.other = value



    def send(self, msg):
        try:
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(message)
            recieved = self.client.recv(1024).decode(FORMAT)
            self.recieve(recieved)
        except:
            # print('send error')
            pass

    def set_self(self, player):
        self.player = player
        self.send(json.dumps(self.player))

    def get_other(self, id):
        self.set_self(self.player)



class Game:
    def __init__(self):
        pygame.init()
        # self.screen = pygame.display.set_mode((WIDTH, HEIGTH),  pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Shooter Game')
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(-1)        # Plays six times, not five!
        # pygame.mixer.music.queue('mozart.ogg')
        self.ui = UI()

        self.running = True
        self.highest_kills = 0
        self.level = Level(self.highest_kills, None)
        self.playing = False
        self.seconds = 0
        self.lastSecond = 0
        self.state = {}

        self.network = Network()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.network.send(DISCONNECT_MESSAGE)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.playing = False
                        self.ui.open = not self.playing
                        self.ui.restart = True

            self.playing = not self.ui.open
            if self.level.killed:
                self.level = Level(self.highest_kills, self.level.id)
                self.seconds = 0
            if self.playing:
                self.ui.stop()
                self.screen.fill('#863a3a')
                if pygame.time.get_ticks() - self.lastSecond > 1000:
                    self.seconds+=1
                    self.lastSecond = pygame.time.get_ticks()
                if self.level.highest_kills > self.highest_kills:
                    self.highest_kills = self.level.highest_kills
                self.level.run(self.dt, self.seconds, self.network)


            else:
                self.screen.fill('#ff4242')
                self.ui.run(self.level.state)


            pygame.display.update()
            # self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
