from random import choice
import random
import pygame, math
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos, groups, player,player2,  player_kill, obstacle_sprites, create_particle, level, id):
        super().__init__(groups)
        self.level = level
        self.id = id
        self.level.zom_ids.append(self.id)
        self.display_surface = pygame.display.get_surface()

        self.obstacle_sprites = obstacle_sprites
        self.create_particle = create_particle
        self.type = 'enemy'

        self.original_image = pygame.transform.rotozoom(pygame.image.load('zombie.png').convert_alpha(), 0,1)

        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(center=pos)

        self.original_rect = self.original_image.get_rect(center=pos)

        self.hitbox = self.rect

        self.width = self.original_rect.width
        self.height = self.original_rect.height

        self.time2particle = pygame.time.get_ticks()
        self.health = 100
        self.killed = False

        
        # self.hitbox = self.rect.inflate(0, -10)
        # self.image.fill('green')
        self.player = player
        self.player2 =player2
        self.players = [self.player, self.player2]

        self.player_kill = player_kill

        self.offset_pos = pygame.math.Vector2(0,0)

        self.directionMove = pygame.math.Vector2(self.player.rect.centerx, self.player.rect.centery).normalize()
        self.speed = 300
        self.prev_pos = self.hitbox.center

        self.health_rect_height = 24
        self.health_rect_width = 100
        self.health_rect_color = '#863a3a'
        self.health_rect = pygame.Rect(self.offset_pos.x - self.health_rect_width/6, self.offset_pos.y - self.health_rect_height, self.health_rect_width, self.health_rect_height)

        self.health2_rect_height = 24
        self.health2_rect_width = self.health
        self.health2_rect_color = pygame.Color(249, 78, 78)
        self.health2_rect = pygame.Rect(self.offset_pos.x - self.health_rect_width/6, self.offset_pos.y - self.health2_rect_height, self.health2_rect_width, self.health2_rect_height)
        self.level.zombies.append(self)
        self.directionMove2 = pygame.math.Vector2()
    def move(self, dt):
        self.prev_pos = self.hitbox.center
        player_x1, player_y1 = self.player.hitbox.center
        if self.player2 != None:
            player_x2, player_y2 = self.player2.hitbox.center
            self.directionMove2 = pygame.math.Vector2(player_x2 - self.rect.centerx, player_y2 - self.rect.centery)
        print(self.player2)

        player_x, player_y = self.player.offset_pos
        rel_x, rel_y = player_x - self.offset_pos.x, player_y - self.offset_pos.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.directionMouse = pygame.math.Vector2(rel_x, rel_y)
        if self.directionMouse.magnitude() != 0:
            self.directionMouse = self.directionMouse.normalize()
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        # self.hitbox = self.rect.inflate(-30, -30)

        self.original_rect.center = self.rect.center

        x = math.sqrt((self.width*self.width) - (abs(math.cos(angle))* self.width*abs(math.cos(angle))* self.width))
        y = self.height * abs(math.cos(angle))* self.width / self.width

        self.height2 = x+y

        # self.hitbox = self.original_rect.inflate(-1*(self.width -(abs(math.cos(angle))* self.width))+10, self.height2 - self.height-10)
        self.hitbox = self.original_rect.copy()


        self.directionMove = pygame.math.Vector2(player_x1 - self.rect.centerx, player_y1 - self.rect.centery)
        if self.player2:
            if self.directionMove.magnitude() > self.directionMove2.magnitude(): self.directionMove = self.directionMove2
            else: self.directionMove = self.directionMove
        if self.directionMove.magnitude() != 0:
            self.directionMove = self.directionMove.normalize()

        self.hitbox.centerx += self.directionMove.x*dt*self.speed
        self.collision('h')
        self.hitbox.centery += self.directionMove.y*dt*self.speed
        self.collision('v')
        self.rect = self.image.get_rect(center=self.hitbox.center)


    def player_collision(self, player):
        if self.hitbox.colliderect(player.hitbox):
            self.player_kill()

    def collision(self, type):
        if type == 'h':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if(sprite.type == 'block'):
                        self.hitbox.centerx = self.prev_pos[0]
                        # if self.direction.x > 0:
                        #     self.hitbox.right = sprite.hitbox.left
                        # if self.direction.x < 0:
                        #     self.hitbox.left = sprite.hitbox.right

                        # if self.hitbox.right >= sprite.hitbox.left and self.directionMove.x  > 0 and sprite.hitbox.bottom >= self.hitbox.centery >= sprite.hitbox.top:
                        #     self.hitbox.right -= self.hitbox.right - sprite.hitbox.left
                        # print(1)

                        # if self.hitbox.left <= sprite.hitbox.right and self.directionMove.x < 0  and sprite.hitbox.bottom >= self.hitbox.centery >= sprite.hitbox.top:
                        #     self.hitbox.left += sprite.hitbox.right - self.hitbox.left

        if type == 'v':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if(sprite.type == 'block'):
                        self.hitbox.centery = self.prev_pos[1]
                        # if self.directionMove.y > 0:
                        #     self.hitbox.bottom = sprite.hitbox.top
                        # if self.directionMove.y < 0:
                        #     self.hitbox.top = sprite.hitbox.bottom

                        # if self.hitbox.top <= sprite.hitbox.bottom and self.directionMove.y < 0 and sprite.hitbox.left <= self.hitbox.centerx <= sprite.hitbox.right:
                        #     self.hitbox.top += (sprite.hitbox.bottom - self.hitbox.top)

                        # print(2)
                        # if self.hitbox.bottom >= sprite.hitbox.top and self.directionMove.y > 0 and sprite.hitbox.left <= self.hitbox.centerx <= sprite.hitbox.right:
                        #     self.hitbox.bottom -= (self.hitbox.bottom - sprite.hitbox.top)


    def cooldowns(self, dt):
        if (pygame.time.get_ticks() - self.time2particle > 30):
            self.create_particle(self)
            self.time2particle = pygame.time.get_ticks()


    def checkDied(self, dt):
        if self.health <= 0.1:
            self.killed = True
            self.kill()
            self.player.kills+=1

    def draw_ui(self, dt):
        self.health2_rect_width = self.health
        self.health_rect = pygame.Rect(self.offset_pos.x - self.health_rect_width/6, self.offset_pos.y - self.health_rect_height, self.health_rect_width, self.health_rect_height)
        self.health2_rect = pygame.Rect(self.offset_pos.x - self.health_rect_width/6, self.offset_pos.y - self.health2_rect_height, self.health2_rect_width, self.health2_rect_height)
        pygame.draw.rect(self.display_surface, self.health_rect_color, self.health_rect, 0, 0,20, 5,5,20)
        pygame.draw.rect(self.display_surface, self.health2_rect_color, self.health2_rect, 0, 0,20, 5,5,20)


    def update(self, dt):
        self.move(dt)
        self.cooldowns(dt)
        self.player_collision(self.player)
        self.checkDied(dt)
        self.draw_ui(dt)