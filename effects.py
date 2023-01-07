import random, math
import pygame
from settings import *

class Effects:
	def __init__(self):
		pass

	@staticmethod
	def create_kill_effect(sprite, groups,dt, name):
		for y in range(sprite.rect.top, sprite.rect.bottom+1, 8):
			for x in range(sprite.rect.left, sprite.rect.right+1, 8):
				direction = [random.randint(-1, 1), random.randint(-1, 1)]
				speed = [random.uniform(50, 200), random.uniform(50, 200)]
				r = random.randint(1, 7)
				Particle(pygame.math.Vector2(x, y),groups, direction, speed,r, dt, 'kill_particle', name)

	@staticmethod
	def create_move_effect(sprite, groups,dt, name):
		offsetX = random.choice([-1,1]) *random.uniform(0.1,sprite.width/4)
		offsetY = random.choice([-1,1]) *random.uniform(0.1,sprite.height/4)
		pos =   pygame.math.Vector2(sprite.rect.centerx+offsetX, sprite.rect.centery+offsetY)
		Particle(pos,groups, [0,0], [0,0],0, dt, 'move_particle',name )

		

class Particle(pygame.sprite.Sprite):
	def __init__(self, pos,groups, direction, speed,r, dt, type, name):
		super().__init__(groups)
		self.name = name
		self.type = type
		if self.type == 'kill_particle':
			self.pos = pos
			self.r = r
			self.speed = speed

			self.dt = dt
			self.rect = pygame.Rect(self.pos.x, self.pos.y, self.r, self.r)
			self.alpha = 170
			self.to_keep = 1000

			if self.type == 'kill_particle':
				self.color = pygame.Color(249, 78, 78, self.alpha)
			else : self.color = '#ffffff'
			self.second_color = pygame.Color(134, 58, 58, 0)


			self.target_rect = pygame.Rect(self.rect.center, (0, 0)).inflate((self.r * 2, self.r * 2))
			self.shape_surf = pygame.Surface(self.target_rect.size, pygame.SRCALPHA)


			self.time2hide = 0
			self.last = False

			if direction[0] == 0 and direction[1] == 0 and self.type == 'kill_particle':
				self.direction = [-1, 1]
			else:
				self.direction = direction

		elif self.type == 'move_particle':
			self.pos = pos
			self.r = random.randint(7,12)
			self.speed = speed

			self.dt = dt
			self.rect = pygame.Rect(self.pos.x, self.pos.y, self.r, self.r)
			self.alpha = 200
			if self.name == 'Enemy':
				self.color = pygame.Color(249, 78, 78, self.alpha)
			elif self.name == 'Player':
				self.color = pygame.Color(255,255,255, self.alpha)

			self.target_rect = pygame.Rect(self.rect.center, (0, 0)).inflate((self.r * 2, self.r * 2))
			self.shape_surf = pygame.Surface(self.target_rect.size, pygame.SRCALPHA)


			self.time2hide = 0
			self.to_keep = 2000
			self.last = False

			if direction[0] == 0 and direction[1] == 0 and self.type == 'kill_particle':
				self.direction = [-1, 1]
			else:
				self.direction = direction


	def move(self, dt):
		self.pos.x += self.direction[0] * self.speed[0] * dt
		self.pos.y += self.direction[1] * self.speed[1] * dt
		self.rect = pygame.Rect(self.pos.x, self.pos.y, self.r, self.r)

	def cooldowns(self):
		if(pygame.time.get_ticks() - self.time2hide > self.to_keep):
			self.kill()

	def update(self, dt):
		if self.type == 'kill_particle':
			self.move(dt)
			if self.color[3] > 0:
				self.alpha -= 2
				self.color = pygame.Color(249, 78, 78, self.alpha)
				if(self.time2hide == 0):
					self.time2hide = pygame.time.get_ticks()
		if self.type == 'move_particle':
			self.move(dt)
			if self.color[3] > 0:
				self.alpha -= 2
				if self.name == 'Enemy':
					self.color = pygame.Color(249, 78, 78, self.alpha)
				elif self.name == 'Player':
					self.color = pygame.Color(255,255,255, self.alpha)
				if(self.time2hide == 0):
					self.time2hide = pygame.time.get_ticks()

		self.r -= 10*dt
		self.rect = pygame.Rect(self.pos.x, self.pos.y, self.r, self.r)
		self.target_rect = pygame.Rect(self.rect.center, (0, 0)).inflate((self.r * 2, self.r * 2))
		
		if self.r <= 0:
			self.kill()

		if self.target_rect.width > 0.1 and self.target_rect.height > 0.1:

			self.shape_surf = pygame.Surface(self.target_rect.size, pygame.SRCALPHA)

		self.cooldowns()