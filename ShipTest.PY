import pygame
import random
import sys

leveler = 0
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()
FPS = 200
leveler = 0



screen_width = 800
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])

all_sprites_list = pygame.sprite.Group()
ship_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()


class Game(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

		self.playerShip = Ship()
		ship_list.add(self.playerShip)
		all_sprites_list.add(self.playerShip)



	def update(self):
		global leveler
		if len(enemy_list) == 0:
			enemy = Enemy()
			enemy.respawn()
			leveler += 1
		for enemy in enemy_list:
			ship_hit_list = pygame.sprite.spritecollide(enemy, ship_list, False)

			#if self.playerShip in ship_hit_list:
				#Ship.health -= 1
				#print (Ship.health)
				#if len(ship_list) == 0:
				#	sys.exit()


		screen.fill((0,0,0))
		all_sprites_list.draw(screen)
		self.playerShip.update()
		Scoreboard(leveler)



class Ship(pygame.sprite.Sprite):
	def __init__(self):
		health = 0
		super().__init__()

		Ship.health = 100
		self.image = pygame.image.load('D:\Projects portfolio\PythonStuff\playerShip.png')
		self.rect = self.image.get_rect()
		self.rect.y = screen_height - 100

	def update(self):

		pos = pygame.mouse.get_pos()
		self.rect.x = pos[0]

class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

		self.image = pygame.image.load('D:\Projects portfolio\PythonStuff\shot.png')
		self.rect = self.image.get_rect()

	def update(self):

		self.rect.y -= 10

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

		self.image = pygame.image.load('D:\Projects portfolio\PythonStuff\enemyShip.png')
		self.rect = self.image.get_rect()

	def update(self):

		self.rect.y += 1

		for enemy in enemy_list:
			if self.rect.y > screen_height + 20:
				self.rect.x = random.randrange(0, screen_width - enemy.rect.w)
				self.rect.y = random.randrange(-400, -100)

	def respawn(self):

		for enemies in range(10):
			enemy = Enemy()
			enemy.rect.x = random.randrange(0, screen_width - enemy.rect.w)
			enemy.rect.y = random.randrange(-400, -100)
			all_sprites_list.add(enemy)
			enemy_list.add(enemy)

class Scoreboard(object):
	def __init__(self, level=1):

		self.level = level
		font_size = 15
		self.font = pygame.font.Font('freesansbold.ttf', font_size)
		text_surf = self.font.render('level: %s' %(level), True, WHITE)
		text_rect = text_surf.get_rect()
		screen.blit(text_surf, text_rect)

def main():
	pygame.init()
	pygame.mouse.set_visible(0)
	game = Game()


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				bullet = Bullet()
				bullet.rect.x = game.playerShip.rect.x + 20
				bullet.rect.y = game.playerShip.rect.y - 20
				all_sprites_list.add(bullet)
				bullet_list.add(bullet)

		for bullet in bullet_list:
			enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)

			for enemy in enemy_hit_list:
				bullet_list.remove(bullet)
				all_sprites_list.remove(bullet)

			if bullet.rect.y < -5:
				bullet_list.remove(bullet)
				all_sprites_list.remove(bullet)

		game.update()
		all_sprites_list.update()
		pygame.display.update()
		clock.tick(FPS)

main()
