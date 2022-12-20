from settings import *
import pygame , sys
import random

class UI:
	def __init__(self):
		self.open = True
		self.state = None
		self.display_surface = pygame.display.get_surface()
		self.alpha = 100
		self.main_color = '#ff5353'
		self.main_rect = pygame.Rect(WIDTH/2 - 880/2, HEIGTH/2 - 480/2, 880, 480)

		self.font = pygame.font.Font('main_font.ttf', 50)
		self.font2 = pygame.font.Font('main_font.ttf', 40)
 
		# create a text surface object,
		# on which text is drawn on it.
		self.text = self.font.render('Red Cube Game', True, '#ffffff')
		 
		# create a rectangular object for the
		# text surface object
		self.textRect = self.text.get_rect(center = (WIDTH/2, HEIGTH/2 - 500/2+125))

		# self.button_rect = pygame.Rect(WIDTH/2 - 304/2, HEIGTH/2, 304,179)
		self.button_color = '#ff6565'

		self.button_rect = pygame.Rect(WIDTH/2 - 304/2, HEIGTH/2+75 - 171/2, 304, 90)

		self.restart = False
		if self.restart:
			self.button_text = self.font2.render('Continue', True, '#ffffff')

		else:
			self.button_text = self.font2.render('Play', True, '#ffffff')
		self.button_text_rect = self.button_text.get_rect(center = (WIDTH/2, HEIGTH/2 + 35))

		self.button_exit_rect = pygame.Rect(WIDTH/2 - 304/2, HEIGTH/2+150 - 90/2, 304, 90)
		self.button_exit_text = self.font2.render('Exit', True, '#ffffff')
		self.button_exit_text_rect = self.button_exit_text.get_rect(center = (WIDTH/2, HEIGTH/2+150))
		
		

	def start(self, state):
		self.open = True
		self.state = state
		self.run(self.state)

	def stop(self):
		self.open = False

	def checkPressed(self):
		mouse_pos = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed()[0]
		if mouse_pressed and self.button_rect.collidepoint(*mouse_pos):
			self.stop()

		if mouse_pressed and self.button_exit_rect.collidepoint(*mouse_pos):
			pygame.quit()
			sys.exit()

	def run(self, state):
		if self.open:
			self.state = state
			pygame.draw.rect(self.display_surface, self.main_color, self.main_rect,  0, 3)
			self.display_surface.blit(self.text, self.textRect)
			pygame.draw.rect(self.display_surface, self.button_color, self.button_rect, 0, 20)
			self.display_surface.blit(self.button_text, self.button_text_rect)

			self.checkPressed()
			if self.restart:
				self.button_text = self.font2.render('Continue', True, '#ffffff')

			else:
				self.button_text = self.font2.render('Play', True, '#ffffff')
			self.button_text_rect = self.button_text.get_rect(center = (WIDTH/2, HEIGTH/2+35))

			pygame.draw.rect(self.display_surface, self.button_color, self.button_exit_rect, 0, 20)
			self.display_surface.blit(self.button_exit_text, self.button_exit_text_rect)