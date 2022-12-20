from random import choice
from fractions import Fraction
import pygame, math, sys
from effects import Particle
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self,pos, groups, obstacle_sprites, create_bullet, create_particle, get_seconds, highest_kills):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()

        self.obstacle_sprites = obstacle_sprites
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect
        self.direction = pygame.Vector2()
        self.speed = 400
        self.type = 'player'
        self.offset_pos = 0
        self.angle = 0

        self.collied = False
        self.collieds = {
            'left':False,
            'right':False,
            'top':False,
            'bottom':False,
        }

        self.prev_pos = self.hitbox

        self.can_attack = True

        self.directionMouse = [0,0]
        self.directionNormalized = pygame.math.Vector2(self.direction.x, self.direction.y)

        self.original_image = pygame.transform.rotozoom(pygame.image.load('square.png').convert_alpha(), 0, 1)
        self.original_rect = self.original_image.get_rect(center=pos)

        self.create_bullet = create_bullet
        self.create_particle = create_particle
        self.get_seconds = get_seconds

        self.time2attack = 0
        self.time2particle = 0

        self.width = self.original_rect.width
        self.height = self.original_rect.height

        self.prev_posSX = [self.prev_pos]
        self.prev_posSY = [self.prev_pos]
        self.iX = 0
        self.iY= 0

        self.kills = 0
        self.score = 0
        self.highest_kills = highest_kills

        self.font = pygame.font.Font('main_font.ttf', 40)
 
        # create a text surface object,
        # on which text is drawn on it.
        self.text_score = self.font.render(f'Score: {self.score}', True, '#ffffff')
         
        # create a rectangular object for the
        # text surface object
        self.text_scoreRect = self.text_score.get_rect(topleft = (10,10))

        # create a text surface object,
        # on which text is drawn on it.
        self.text_kills = self.font.render(f'Kills: {self.kills}', True, '#ffffff')
         
        # create a rectangular object for the
        # text surface object
        self.text_killsRect = self.text_kills.get_rect(topleft = (10,64))

        self.text_highest_kills = self.font.render(f'Highest Kills: {self.highest_kills}', True, '#ffffff')
         
        # create a rectangular object for the
        # text surface object
        self.text_highest_killsRect = self.text_highest_kills.get_rect(topleft = (10,128))


    def input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a] and not self.collieds['left']:
            self.direction.x = -1
        elif pressed[pygame.K_d] and not self.collieds['right']:
            self.direction.x = 1
        else:
            self.direction.x = 0



        if pressed[pygame.K_w] and not self.collieds['top']:
            self.direction.y = -1
        elif pressed[pygame.K_s] and not self.collieds['bottom']:
            self.direction.y = 1
        else:
            self.direction.y = 0
            

        if pygame.mouse.get_pressed()[0] and self.can_attack:
            self.create_bullet((self.rect.centerx, self.rect.centery), self.directionMouse, self.angle)
            self.time2attack = pygame.time.get_ticks()
            self.can_attack = False


    def collision(self, type):
        if type == 'h':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # if self.prev_posSX[-1].right < sprite.hitbox.left and self.hitbox.right > sprite.hitbox.left or self.direction.x == 1:
                    #     self.hitbox.right = self.prev_posSX[-1].right
                    #     self.prev_posSX.pop()
                    #     self.prev_posSX.append(self.hitbox.copy())
                    #     self.collision('h')
                    #     self.collieds['right'] = True
                    # else:
                    #     self.collieds['right'] = False

                    # if self.prev_posSX[-1].left > sprite.hitbox.right and self.hitbox.left < sprite.hitbox.right or self.direction.x == -1:
                    #     self.hitbox.left = self.prev_posSX[-1].left
                    #     self.prev_posSX.pop()
                    #     self.prev_posSX.append(self.hitbox.copy())
                    #     self.collision('h')
                    #     self.collieds['left'] = True
                    # else:
                    #     self.collieds['left'] = False


                    if self.hitbox.right > sprite.hitbox.left and self.direction.x == 1 and sprite.hitbox.bottom > self.hitbox.centery > sprite.hitbox.top:
                        self.hitbox.right -= self.hitbox.right - sprite.hitbox.left
                        print(1)

                        self.collieds['right'] = True
                    if self.hitbox.left < sprite.hitbox.right and self.direction.x == -1  and sprite.hitbox.bottom > self.hitbox.centery > sprite.hitbox.top:
                        self.hitbox.left += sprite.hitbox.right - self.hitbox.left

                        print(-1)
                        self.collieds['left'] = True

                else:
                    self.collieds['right'] = False
                    self.collieds['left'] = False


        if type == 'v':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # if self.prev_posSY[-1].top > sprite.hitbox.bottom and self.hitbox.top < sprite.hitbox.bottom or self.direction.y == -1:
                    #     self.hitbox.top = self.prev_posSY[-1].top
                        
                    #     self.prev_posSY.pop()
                    #     self.collision('v')
                    #     self.collieds['top'] = True
                    # else:
                    #     self.collieds['top'] = False
                    # if self.prev_posSY[-1].bottom < sprite.hitbox.bottom and self.hitbox.bottom > sprite.hitbox.bottom or self.direction.y == 1:
                    #     self.hitbox.bottom = self.prev_posSY[self.iY].bottom
                    #     self.prev_posSY.pop()
                    #     self.collision('v')
                    #     self.collieds['bottom'] = True
                    # else:
                    #     self.collieds['bottom'] = False


                    if self.hitbox.top < sprite.hitbox.bottom and self.direction.y == -1 and sprite.hitbox.left < self.hitbox.centerx < sprite.hitbox.right:
                        self.hitbox.top += (sprite.hitbox.bottom - self.hitbox.top)

                        print(2)
                        self.collieds['top'] = True
                    if self.hitbox.bottom > sprite.hitbox.top and self.direction.y == 1 and sprite.hitbox.left < self.hitbox.centerx < sprite.hitbox.right:
                        self.hitbox.bottom -= (self.hitbox.bottom - sprite.hitbox.top)

                        print(-2)
                        self.collieds['bottom'] = True

                else:
                    self.collieds['top'] = False
                    self.collieds['bottom'] = False

    def simplify(self, n, d):
        i = min(n, d)
        j = 2
        while j < i+1:
            if n % j == 0 and d % j == 0:
                n = n // j
                d = d // j
            else:
                j+=1
        return pygame.math.Vector2(d, n)



    def move(self, dt):
        self.prev_pos = self.hitbox.copy()
        self.prev_posSX.append(self.prev_pos.copy())
        self.prev_posSY.append(self.prev_pos.copy())
        self.iX = len(self.prev_posSX) -1
        self.iY = len(self.prev_posSY) -1
        if self.direction.magnitude() != 0:
            self.directionNormalized = self.direction.normalize()
        else :
            self.directionNormalized = self.direction
        self.hitbox.x += self.directionNormalized.x * self.speed * dt
        self.collision('h')
        self.hitbox.y += self.directionNormalized.y * self.speed * dt
        self.collision('v')
        self.rect.center = self.hitbox.center

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.offset_pos.x, mouse_y - self.offset_pos.y
        self.directionMouse = self.simplify(rel_y, rel_x)
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.hitbox.center)

        self.original_rect.center = self.rect.center

        self.hitbox = self.rect


    def cooldowns(self):
        if(pygame.time.get_ticks() - self.time2attack > 500):
            self.can_attack = True
        else:
            self.can_attack = False

        if (pygame.time.get_ticks() - self.time2particle > 20):
            self.create_particle(self)
            self.time2particle = pygame.time.get_ticks()


    def draw_ui(self):
        self.text_highest_kills = self.font.render(f'Highest Kills: {self.highest_kills}', True, '#ffffff')
        self.score = self.get_seconds()
        self.text_score = self.font.render(f'Score: {self.score}', True, '#ffffff')
        self.text_kills = self.font.render(f'Kills: {self.kills}', True, '#ffffff')
        self.display_surface.blit(self.text_score, self.text_scoreRect)
        self.display_surface.blit(self.text_kills, self.text_killsRect)
        self.display_surface.blit(self.text_highest_kills, self.text_highest_killsRect)

    def update(self, dt):
        self.dt = dt
        self.cooldowns()
        self.input()
        self.move(dt)

        self.draw_ui()