import pygame, sys, random
from settings import *
from level import Level
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH),  pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Shooter Game')
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(-1)        # Plays six times, not five!
        # pygame.mixer.music.queue('mozart.ogg')
        self.ui = UI()

        self.running = True
        self.highest_kills = 0
        self.level = Level(self.highest_kills)
        self.playing = False
        self.seconds = 0
        self.lastSecond = 0
        self.state = {}

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.playing = False
                        self.ui.open = not self.playing
                        self.ui.restart = True

            self.playing = not self.ui.open
            if self.level.killed:
                self.level = Level(self.highest_kills)
                self.seconds = 0
            if self.playing:
                self.ui.stop()
                self.screen.fill('#863a3a')
                if pygame.time.get_ticks() - self.lastSecond > 1000:
                    print('wow')
                    self.seconds+=1
                    self.lastSecond = pygame.time.get_ticks()
                if self.level.highest_kills > self.highest_kills:
                    self.highest_kills = self.level.highest_kills
                self.level.run(self.dt, self.seconds)

            else:
                self.screen.fill('#ff4242')
                self.ui.run(self.level.state)


            pygame.display.update()
            # self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
