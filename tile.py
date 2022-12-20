from random import choice
import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos, groups, type):
        super().__init__(groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(center = pos)
        self.image.fill('black')
        self.type = type
        self.hitbox = self.rect
        # self.hitbox = self.rect