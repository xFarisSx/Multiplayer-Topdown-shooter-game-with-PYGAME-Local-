import random, math
import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos,groups, direction, rotation, obstacle_sprites, create_kill_effect):
		super().__init__(groups)


		self.collieds = {
            'left':False,
            'right':False,
            'top':False,
            'bottom':False,
        }

		direction = pygame.math.Vector2(direction[0], direction[1])
		self.create_kill_effect = create_kill_effect
		# self.pos = pos
		if direction.magnitude() != 0:
			self.direction = direction.normalize()
		else:
			self.direction = pygame.math.Vector2(0,0)
		self.speed = 15

		self.pos = (pos[0] + (TILESIZE/1.2*self.direction.x), pos[1]+ (TILESIZE/1.2* self.direction.y))

		self.original_image = pygame.transform.rotozoom(pygame.image.load('square.png').convert_alpha(), 0, 1)
		self.original_image = pygame.transform.scale_by(self.original_image, (0.5, 0.2))
		self.original_rect = self.original_image.get_rect(center=self.pos)

		self.rotation = rotation
		self.image = pygame.transform.rotozoom(self.original_image, self.rotation, 1)
		self.rect = self.image.get_rect(center=self.pos)
		self.time2 = pygame.time.get_ticks()

		self.obstacle_sprites = obstacle_sprites
		# self.hitbox = self.rect.inflate(-10, -10)
		self.hitbox = self.rect

		self.width = self.original_rect.width
		self.height = self.original_rect.height

		self.power = 50

	def move(self, dt):
		self.rect.x+= self.speed*self.direction.x 
		self.rect.y+= self.speed*self.direction.y 
		self.original_rect.center = self.rect.center

		x = math.sqrt((self.width*self.width) - (abs(math.cos(self.rotation))* self.width*abs(math.cos(self.rotation))* self.width))
		y = self.height * abs(math.cos(self.rotation))* self.width / self.width

		self.height2 = x+y

		self.hitbox = self.original_rect.inflate(-1*(self.width -(abs(math.cos(self.rotation))* self.width)), self.height2 - self.height)

		
	def cooldowns(self):
		if(pygame.time.get_ticks() - self.time2 > 2000):
			self.kill()


	def collision(self):
		for sprite in self.obstacle_sprites.sprites():
			if sprite.hitbox.colliderect(self.hitbox):
				if sprite.__class__.__name__ == 'Enemy':
					self.create_kill_effect(sprite)
					sprite.health -= self.power
					self.kill()

				if self.hitbox.right >= sprite.hitbox.left and self.direction.x > 0 and sprite.hitbox.bottom >= self.hitbox.centery >= sprite.hitbox.top:
					self.hitbox.right -= self.hitbox.right - sprite.hitbox.left
					self.collieds['right'] = True
				else:
					self.collieds['right'] = False
				if self.hitbox.left <= sprite.hitbox.right and self.direction.x < 0  and sprite.hitbox.bottom >= self.hitbox.centery >= sprite.hitbox.top:
					self.hitbox.left += sprite.hitbox.right - self.hitbox.left
					self.collieds['left'] = True
				else:
					self.collieds['left'] = False

				if self.hitbox.top <= sprite.hitbox.bottom and self.direction.y < 0 and sprite.hitbox.left <= self.hitbox.centerx <= sprite.hitbox.right:
					self.hitbox.top += (sprite.hitbox.bottom - self.hitbox.top)
					self.collieds['top'] = True
				else:
					self.collieds['top'] = False

				if self.hitbox.bottom >= sprite.hitbox.top and self.direction.y > 0 and sprite.hitbox.left <= self.hitbox.centerx <= sprite.hitbox.right:
					self.hitbox.bottom -= (self.hitbox.bottom - sprite.hitbox.top)
					self.collieds['bottom'] = True
				else:
					self.collieds['bottom'] = False

				if self.collieds['bottom'] or self.collieds['top']:
					self.direction.y *= -1
				if self.collieds['left'] or self.collieds['right']:
					self.direction.x *= -1

				self.rotation = (180 / math.pi) * -math.atan2(self.direction.y, self.direction.x)

				self.image = pygame.transform.rotate(self.original_image, int(self.rotation))
				self.rect = self.image.get_rect(center=self.hitbox.center)
				self.original_rect.center = self.rect.center
				self.hitbox = self.rect



	def update(self, dt):
		self.collision()
		self.move(dt)
		self.cooldowns()