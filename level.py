import random
import pygame
from settings import *
from player import Player
from enemy import Enemy
from tile import Tile
from bullet import Bullet
from effects import Effects


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.window_height = self.display_surface.get_height()
        self.window_width = self.display_surface.get_width()
        self.offset = pygame.math.Vector2()
        self.box_coord = {'left':575, 'top':300, 'right':575, "bottom":300}
        l = self.box_coord['left']
        t = self.box_coord['top']
        w = self.window_width - (l + self.box_coord['right'])
        h = self.window_height - (t + self.box_coord['bottom'])
        self.box_rect = pygame.Rect(l,t,w,h)
        self.light= pygame.transform.rotozoom(pygame.image.load('light.png').convert_alpha(), 0, 5)
        self.light.set_alpha(500)
        self.light2= pygame.transform.rotozoom(pygame.image.load('light.png').convert_alpha(), 0, 1.4)
        self.light2.set_alpha(50)
        



    def custom_draw(self, player):
        self.box_target_camera(player)

        for sprite in self.sprites():
            if sprite.__class__.__name__ == 'Particle':
                    offset_pos = sprite.pos - self.offset

                    pygame.draw.circle(sprite.shape_surf, sprite.color, (sprite.r, sprite.r), sprite.r)
                    withoffset = sprite.target_rect.copy()
                    withoffset.topleft = offset_pos
                    self.display_surface.blit(sprite.shape_surf, withoffset)

                    # pygame.draw.circle(sprite.display_surface, sprite.color, offset_pos, sprite.r)
                    sprite.offset_pos = offset_pos
        

        for sprite in sorted(self.sprites(),key= lambda sprite: sprite.rect.centery):
            if sprite.__class__.__name__ == 'Player':
                offset_pos = sprite.rect.topleft - self.offset
                offset_pos2 = sprite.rect.center - self.offset
                self.display_surface.blit(sprite.image,offset_pos)
                sprite.offset_pos = offset_pos2
                # print(1)
                continue
            if sprite.__class__.__name__ == 'Enemy':
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image,offset_pos)
                sprite.offset_pos = offset_pos
                # print(1)
                continue
            if sprite.__class__.__name__ == 'Particle':
                # offset_pos = sprite.pos - self.offset
                # # self.display_surface.blit(sprite.image,offset_pos)
                # pygame.draw.circle(self.display_surface, sprite.color, offset_pos, sprite.r)
                # sprite.offset_pos = offset_pos
                # # print(1)
                continue

            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

            

        # pygame.draw.rect(self.display_surface, 'green', self.box_rect, 5)
        # for sprite in self.sprites():
        #     if sprite.__class__.__name__ == 'Particle':
        #             offset_pos = sprite.pos - self.offset

        #             pygame.draw.circle(sprite.shape_surf, sprite.color, (sprite.r, sprite.r), sprite.r)
        #             withoffset = sprite.target_rect.copy()
        #             withoffset.topleft = offset_pos
        #             self.display_surface.blit(sprite.shape_surf, withoffset)

        #             # pygame.draw.circle(sprite.display_surface, sprite.color, offset_pos, sprite.r)
        #             sprite.offset_pos = offset_pos


        # redF
        filter = pygame.surface.Surface((WIDTH, HEIGTH))
        filter2 = pygame.surface.Surface((WIDTH, HEIGTH))
        # filter.fill(pygame.color.Color('#d28787'))
        # filter2.fill(pygame.color.Color('#d28787'))
        filter.blit(self.light, (player.offset_pos.x - self.light.get_width()/2-20, player.offset_pos.y - self.light.get_height()/2))
        filter2.blit(self.light2, (player.offset_pos.x - self.light2.get_width()/2-20, player.offset_pos.y - self.light2.get_height()/2))
        self.display_surface.blit(filter, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        self.display_surface.blit(filter2, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
                    


    def box_target_camera(self, target):

        if target.rect.right > self.box_rect.right:
            self.box_rect.right = target.rect.right
        if target.rect.left < self.box_rect.left:
            self.box_rect.left = target.rect.left
        if target.rect.top < self.box_rect.top:
            self.box_rect.top = target.rect.top
        if target.rect.bottom > self.box_rect.bottom:
            self.box_rect.bottom = target.rect.bottom

        self.offset.x =  self.box_rect.x - self.box_coord['left']
        self.offset.y =  self.box_rect.y - self.box_coord['top']


class Level():
    def __init__(self, highest_kills, id, network):
        if id:
            self.id = id
        else: self.id = random.randint(0,1000)

        self.display_surface = pygame.display.get_surface()
        self.window_height = self.display_surface.get_size()[1]
        self.window_width = self.display_surface.get_size()[0]

        self.can_respone = True
        self.time2enemy = 1


        self.visible_sprites = YSortCameraGroup()
        self.bullets = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player = None

        self.dt = 1
        self.highest_kills = highest_kills

        self.create_map()
        self.state = {}

        self.killed = False

        self.can_set = True
        self.can_get = True
        self.time2set = 0
        self.time2get = 0
        self.network = ''
        self.other = ''
        self.player2 = None

        self.zombies = []
        self.zom_ids = []
        self.network = network

    def create_map(self):
        for row_index, row in enumerate(MAP):
            for col_index, col in enumerate(row):
                if col != '':
                    x = (col_index)*(TILESIZE)
                    y = (row_index)*TILESIZE
                    if col == '4':
                        Tile((x-500, y-500), [self.visible_sprites,self.obstacle_sprites], 'block')
        self.player = Player((self.window_width/2, self.window_height/2), [self.visible_sprites], self.obstacle_sprites, self.create_bullet, self.create_particle, self.get_seconds, self.highest_kills, 'main')

    def create_bullet(self, pos, direction, rotation):
        Bullet(pos,[self.visible_sprites, self.bullets], direction, rotation, self.obstacle_sprites, self.create_kill_effect)

    def create_particle(self, sprite):
        Effects.create_move_effect(sprite,[self.visible_sprites], self.dt, sprite.__class__.__name__)

    def create_kill_effect(self, sprite):
        Effects.create_kill_effect(sprite,[self.visible_sprites] ,self.dt, sprite.__class__.__name__)


    def respone_enemy(self):
        
        # if(self.can_respone):
        #     x = random.randint(TILESIZE+32, MAPWIDTH - 600)
        #     y = random.randint(TILESIZE+32, MAPHEIGTH - 500)

        #     for sprite in self.visible_sprites:
        #         if sprite.rect.colliderect(pygame.Rect(x - TILESIZE/2, y - TILESIZE/2, TILESIZE,TILESIZE)):
        #             return
        #     if pygame.Rect(x- TILESIZE/2, y- TILESIZE/2, TILESIZE,TILESIZE).colliderect(pygame.Rect(self.player.rect.x-TILESIZE*8/2, self.player.rect.y - TILESIZE*8/2, TILESIZE*8,TILESIZE*8)):
        #         return
                    
        #     Enemy((x, y), [self.visible_sprites,self.obstacle_sprites], self.player, self.player_kill, self.obstacle_sprites, self.create_particle)
        #     self.can_respone = False
        #     self.time2enemy = pygame.time.get_ticks()

        # if self.zombies == []:
        #     if self.network.zombies != []:
        #         for zom in self.network.zombies:
        #             Enemy(zom['pos'], [self.visible_sprites, self.obstacle_sprites], self.players[0],self.players[1],  self.player_kill, self.obstacle_sprites, self.create_particle, self.level, zom['id'])

        if(self.can_respone):

            self.network.make_zombies(self.visible_sprites, self.obstacle_sprites, self.player_kill, self.create_particle, [self.player, self.player2])

            self.can_respone = False
            self.time2enemy = pygame.time.get_ticks()
        


    def update_zombies(self):
        for zom in self.zombies:
            for i,network_zom in enumerate(self.network.zombies):
                if network_zom['id'] == zom.id:
                    self.network.zombies[i]['pos'] = zom.rect.topleft
                    self.network.zombies[i]['killed'] = zom.killed
            zom.player2 = self.player2


    def player_kill(self):
        self.player.kill()
        self.killed = True
            

    def cooldowns(self):
        if pygame.time.get_ticks() - self.time2enemy > 1000:
            self.can_respone = True
        else:
            self.can_respone = False

        # if pygame.time.get_ticks() - self.time2set > 0:
        #     self.can_set = True
        # else:
        #     self.can_set = False
        # if pygame.time.get_ticks() - self.time2get > 0:
        #     self.can_get = True
        # else:
        #     self.can_get = False

    def get_seconds(self):
        return self.seconds

    def set_self(self):

        player = {
                'id':self.id,
                'pos':(self.player.rect.x, self.player.rect.y)
            }
        self.network.set_self(player)

    def get_other(self):

        self.network.get_other(self.id)
        if self.network.other != '':
            self.other = self.network.other
            if not self.player2:
                self.player2 = Player((self.other['pos'][0], self.other['pos'][1]), [self.visible_sprites], self.obstacle_sprites, self.create_bullet, self.create_particle, self.get_seconds, self.highest_kills, 'other')

    def update_other(self):
        if self.player2:
            self.player2.rect.x = self.other['pos'][0]
            self.player2.rect.y = self.other['pos'][1]


    def run(self, dt, seconds, network):
        self.network = network
        if self.player.kills > self.highest_kills:
            self.highest_kills = self.player.kills
            self.player.highest_kills = self.highest_kills

        self.dt = dt
        self.seconds = seconds
        self.respone_enemy()
        self.cooldowns()
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update(dt)

        self.set_self()
        self.get_other()
        self.update_other()
        self.update_zombies()
        print(self.zom_ids)