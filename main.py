import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
import time
import random
from random import randint

import asyncio


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
pygame.font.init()
my_font = pygame.font.Font('Pictures/Peepo.ttf', 50)
text_surface = my_font.render("Slime of Time", False, (0,0,0))
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Slime of Time')
clock = pygame.time.Clock()
sky = pygame.image.load('Pictures/sky.png')
sky = pygame.transform.scale(sky,(1000,1000))
white = (255,255,255)
restart_img = pygame.image.load('Pictures/restartbtn.png')
restart_img.set_colorkey(white)
restart_img = pygame.transform.scale(restart_img,(50,50))
tile_size = 50
game_over = False
pause_menu = False
win = False
level = 1
start_img = pygame.image.load('Pictures/start.png')
character = 1
exit_img = pygame.image.load('Pictures/exit.png')
pause_img = pygame.image.load('Pictures/pause.png')
exit_img.set_colorkey(white)
recording = False
playback = False
playback_index = 0
recorded_events = []
start_img = pygame.transform.scale(start_img, (300,150))
exit_img = pygame.transform.scale(exit_img,(300,150))
pause_img = pygame.transform.scale(pause_img,(50,50))
main_menu = True
player = 1
switch = False

#SOUNDS
fallfx = pygame.mixer.Sound('Pictures/fall.wav')
fallfx.set_volume(.4)
jumpfx = pygame.mixer.Sound('Pictures/jump.wav')
jumpfx.set_volume(.5)
switchfx = pygame.mixer.Sound('Pictures/onswitch.mp3')
switchfx.set_volume(.3)


class World():
		def __init__(self,data):
			self.tile_list = []
			self.killblocks = []
			self.winblocks = []
			self.spawnpoint = []
			self.botspawnpoint = []
			self.switches = []
			self.switchhitboxes = []
			self.wall = []
			self.walloppo = []
			dirt = pygame.image.load('Pictures/ground.png')
			concrete = pygame.image.load('Pictures/concrete.png')
			botportal = pygame.image.load('Pictures/botportal.png')
			row_count = 0
			for row in data:
				col_count = 0
				for tile in row:
					if tile == 1:
						img = pygame.transform.scale(dirt,(tile_size,tile_size))
						img_rect = img.get_rect()
						img_rect.x = col_count * tile_size
						img_rect.y = row_count * tile_size
						tile = (img, img_rect)
						self.tile_list.append(tile)
					if tile == 2:
						img = pygame.transform.scale(concrete,(tile_size,tile_size))
						img_rect = img.get_rect()
						img_rect.x = col_count * tile_size
						img_rect.y = row_count * tile_size
						tile = (img, img_rect)
						self.tile_list.append(tile)
					if tile == 3:
						self.killblock = pygame.image.load('Pictures/killblock.png')
						self.killblock = pygame.transform.scale(self.killblock,(tile_size,tile_size))
						img_rect = self.killblock.get_rect()
						img_rect.x = col_count * tile_size
						img_rect.y = row_count * tile_size
						
						self.killblocks.append(img_rect)
					if tile == 4:
						self.winblock = pygame.image.load('Pictures/gate.png')
						self.winblock = pygame.transform.scale(self.winblock,(tile_size,tile_size))
						img_rect = self.winblock.get_rect()
						img_rect.x = col_count * tile_size
						img_rect.y = row_count * tile_size

						self.winblocks.append(img_rect)
					if tile == 5:
						
						portal = pygame.image.load('Pictures/portal.png')
						portal.set_colorkey(white)
						self.portal = pygame.transform.scale(portal,(tile_size + 40,tile_size*2))
						img_rect = self.portal.get_rect()
						img_rect.x = col_count * tile_size - 20
						img_rect.y = row_count * tile_size - 20
						self.spawnpoint.append(img_rect)
					if tile == 6:
						botportal = pygame.image.load('Pictures/botportal.png')
						botportal.set_colorkey(white)
						self.botportal = pygame.transform.scale(botportal,(tile_size + 40,tile_size*2))
						img_rect = self.botportal.get_rect()
						img_rect.x = col_count * tile_size - 20
						img_rect.y = row_count * tile_size - 20

						self.botspawnpoint.append(img_rect)
					if tile == 7:
						img = pygame.image.load('Pictures/OFFSWITCH.png')
						self.switch = pygame.transform.scale(img,(tile_size * 4,tile_size * 4))
						img_rect = self.switch.get_rect()
						img_rect.x = col_count * tile_size - 70
						img_rect.y = row_count * tile_size - 60
						self.switchhitbox = Rect(0, 0, 38, 20)
						self.switchhitbox.x = col_count * tile_size + 10
						self.switchhitbox.y = row_count * tile_size + 30
						self.switches.append(img_rect)
						self.switchhitboxes.append(self.switchhitbox)
					if tile == 8:
						img = pygame.image.load('Pictures/wall.png')
						self.wallimg = pygame.transform.scale(img,(tile_size,tile_size))
						img_rect = self.wallimg.get_rect()
						img_rect.x = col_count * tile_size
						img_rect.y = row_count * tile_size
						self.wall.append(img_rect)
					if tile == 9:
						img = pygame.image.load('Pictures/walloppo.png')
						self.wallimgoppo = pygame.transform.scale(img,(tile_size,tile_size))
						img_rect = self.wallimgoppo.get_rect()
						img_rect.x = col_count * tile_size
						img_rect.y = row_count * tile_size
						self.walloppo.append(img_rect)
					col_count += 1
				row_count += 1
		def draw(self):
				for tile in self.tile_list:
					screen.blit(tile[0],tile[1])
				for tile in self.killblocks:
					screen.blit(self.killblock, tile)
				for tile in self.winblocks:
					screen.blit(self.winblock, tile)
				for tile in self.spawnpoint:
					screen.blit(self.portal, tile)
				for tile in self.botspawnpoint:
					screen.blit(self.botportal, tile)
				for tile in self.switches:
					screen.blit(self.switch, tile)
				if switch == False:
					for tile in self.wall:
						screen.blit(self.wallimg,tile)
				if switch == True:
					for tile in self.walloppo:
						screen.blit(self.wallimgoppo,tile)



	


sprite_sheet = pygame.image.load('Pictures/slime spritesheet calciumtrice.png').convert_alpha()

black = (0,0,0)







def get_image(sheet, frame, width, height, scale, color,row):
		image = pygame.Surface((width,height)).convert_alpha()
		image.blit(sheet, (0,0), (32 * frame,row * 32,width,height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(color)
		return image

main_menu_slime = [] 
for num in range(9):
	menu_slime = get_image(sprite_sheet,num,32,32,20,black,5)
	main_menu_slime.append(menu_slime)
main_menu_slime2 = [] 
for num in range(9):
	menu_slime = get_image(sprite_sheet,num,32,32,20,black,2)
	menu_slime = pygame.transform.flip(menu_slime, True, False)
	menu_slime.set_colorkey(black)
	main_menu_slime2.append(menu_slime)



class Button():
	def __init__(self,x,y,image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False



	def draw(self):
		action = False

		#get mouse pos
		pos = pygame.mouse.get_pos()

		#check mouse and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				switchfx.play()
				self.clicked = True
				action = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False



		#draw button
		screen.blit(self.image,self.rect)

		return action


win1 = False
win2 = False
sound = False
ready = True
sound2 = False
ready2 = False




class Player():
	def __init__(self,x,y):
		self.movements = []
		self.reset(x,y)

	def reset(self, x, y):
		self.images_idle_right = []
		self.images_idle_left = []
		self.images_die_left = []
		self.images_die_right = []
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(9):
			img_idle = get_image(sprite_sheet,num,32,32,3,black,5)
			
			img_flip = pygame.transform.flip(img_idle, True, False)
			img_flip.set_colorkey(black)
			self.images_idle_left.append(img_idle)
			self.images_idle_right.append(img_flip)
		for num in range(9):
			img_left = get_image(sprite_sheet,num,32,32,3,black,6)
			img_right = pygame.transform.flip(img_left, True, False)
			img_right.set_colorkey(black)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		for num in range(9):
			img_jump = get_image(sprite_sheet,num,32,32,3,black,9)
			img_jumpflip = pygame.transform.flip(img_jump, True, False)
			img_jumpflip.set_colorkey(black)
			self.images_die_right.append(img_jumpflip)
			self.images_die_left.append(img_jump)
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		#make a smaller rect for hitbox and update it 
		self.hitbox = Rect(0, 0, 38, 32)
		self.hitbox.x = x + 30
		self.hitbox.y = y + 65
		self.rect.x = x
		self.rect.y = y
		self.width = 38
		self.height =32
		self.vel_y = 0
		self.direction = 0
		self.left = False
		self.right= True
		self.death = 0
		self.in_air = True
		
		self.move = 0
	def update(self, game_over):
		global pause_menu, character, win1, win2, switch,sound, ready,sound2,ready2
		dx = 0
		dy = 0
		walk_cooldown = 5
		
		if game_over == False and pause_menu == False:

			key = pygame.key.get_pressed()
			
			if key[pygame.K_a] or key[pygame.K_LEFT]:
				dx -= 5
				self.direction = -1
				if dx != 0:
					self.counter += 1
				self.left = True
				self.right = False



			if key[pygame.K_d] or key[pygame.K_RIGHT]:
				dx += 5
				self.direction = 1
				if dx != 0:
					self.counter += 1
				self.right = True
				self.left = False

			if key[pygame.K_d] == False and key[pygame.K_a] == False and key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False or (key[pygame.K_d] and key[pygame.K_a]) or (key[pygame.K_LEFT] and key[pygame.K_RIGHT]):
				
				self.direction = 0
				if self.direction == 0:
					if self.right == True and self.left == False:
						self.counter += 1
						self.image = self.images_idle_right[self.index]
					elif self.left == True and self.right == False:
						self.counter += 1
						self.image = self.images_idle_left[self.index]


			if key[pygame.K_SPACE] and self.in_air == False:
				jumpfx.play()
				self.vel_y = -15
				self.jumped = True



			if self.counter > walk_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			self.in_air = True

			for tile in world.tile_list:
				if tile[1].colliderect(self.hitbox.x + dx, self.hitbox.y, self.width, self.height):
					dx = 0

				if tile[1].colliderect(self.hitbox.x, self.hitbox.y + dy, self.width, self.height):
					if self.vel_y < 0:

						dy = tile[1].bottom - self.hitbox.top
						self.vel_y = 0
					elif self.vel_y >= 0:

						dy = tile[1].top - self.hitbox.bottom
						self.vel_y = 0
						self.in_air = False



			for tile in world.killblocks:
				if tile.colliderect(self.hitbox.x, self.hitbox.y + dy, self.width, self.height):
					game_over = True
					win1 = False
					win2 = False

			for tile in world.winblocks:
				if tile.colliderect(self.hitbox.x, self.hitbox.y + dy, self.width, self.height):
					if win1 == False:
						win1 = True

						player.reset(botspawnx,botspawny)
						bot.reset(spawnx,spawny)
					elif win1 == True and bot.ready == True:
						win2 = True
						bot.ready = False
						self.movements = []
			switch = False
			
			for tile in world.switchhitboxes:
				if tile.colliderect(self.hitbox.x, self.hitbox.y + dy, self.width, self.height) or tile.colliderect(bot.hitbox.x, bot.hitbox.y + dy, bot.width, bot.height):
					switch = True
					sound = True
					sound2 = False
					ready2 = True
			if sound == True:
				if ready == True:
					switchfx.play()
					ready = False
			if sound2 == True:
				if ready2 == True:
					switchfx.play()
					ready2 = False

			if switch == False:
				ready = True
				sound = False
				sound2 = True
				for tile in world.wall:
					if tile.colliderect(self.hitbox.x + dx, self.hitbox.y, self.width, self.height):
						dx = 0

					if tile.colliderect(self.hitbox.x, self.hitbox.y + dy, self.width, self.height):
						if self.vel_y < 0:
							dy = tile.bottom - self.hitbox.top
							self.vel_y = 0
						elif self.vel_y >= 0:
							dy = tile.top - self.hitbox.bottom
							self.vel_y = 0
							self.in_air = False
			if switch == True:
				
				for tile in world.walloppo:
					if tile.colliderect(self.hitbox.x + dx, self.hitbox.y, self.width, self.height):
						dx = 0

					if tile.colliderect(self.hitbox.x, self.hitbox.y + dy, self.width, self.height):
						if self.vel_y < 0:
							dy = tile.bottom - self.hitbox.top
							self.vel_y = 0
						elif self.vel_y >= 0:
							dy = tile.top - self.hitbox.bottom
							self.vel_y = 0
							self.in_air = False

			
			if win1 == False:
				self.move = (dx,dy)
				self.movements.append(self.move)
			self.rect.x += dx
			self.rect.y += dy
			self.hitbox.x += dx
			self.hitbox.y += dy

		elif game_over == True:
			if self.death == 0:
				self.index = 0
				self.counter = 0
				self.death = 1
			elif self.death == 1:
				walk_cooldown = 7
				if self.left == True and self.right == False:
					self.image = self.images_die_left[self.index]
				elif self.right == True and self.left == False:
					self.image = self.images_die_right[self.index]
				if self.counter > walk_cooldown:
					self.counter = 0
					self.index += 1
					if self.index >= len(self.images_die_right):
						self.index = 8
						

				self.counter += 1

		screen.blit(self.image, self.rect)
		return game_over



class Bot():
	def __init__(self,x,y):

		self.reset(x,y)


	def reset(self, x, y):
		self.images_idle_right = []
		self.images_idle_left = []
		self.images_die_left = []
		self.images_die_right = []
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(9):
			img_idle = get_image(sprite_sheet,num,32,32,3,black,0)
			
			img_flip = pygame.transform.flip(img_idle, True, False)
			img_flip.set_colorkey(black)
			self.images_idle_left.append(img_idle)
			self.images_idle_right.append(img_flip)
		for num in range(9):
			img_left = get_image(sprite_sheet,num,32,32,3,black,1)
			img_right = pygame.transform.flip(img_left, True, False)
			img_right.set_colorkey(black)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		for num in range(9):
			img_jump = get_image(sprite_sheet,num,32,32,3,black,4)
			img_jumpflip = pygame.transform.flip(img_jump, True, False)
			img_jumpflip.set_colorkey(black)
			self.images_die_right.append(img_jumpflip)
			self.images_die_left.append(img_jump)
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		#make a smaller rect for hitbox and update it 
		self.hitbox = Rect(0, 0, 38, 32)
		self.hitbox.x = x + 30
		self.hitbox.y = y + 65
		self.rect.x = x
		self.rect.y = y
		self.width = 38
		self.height =32
		self.vel_y = 0
		self.direction = 0
		self.left = False
		self.right= True
		self.death = 0
		self.in_air = True
		self.control = 0
		self.ready = False
	def update(self, game_over):
		global switch

		walk_cooldown = 5
		if game_over == False and pause_menu == False:
			if win1 == True:
				if self.control < len(player.movements):



					dx = player.movements[self.control][0]
					dy = player.movements[self.control][1]
					if dy == -14:
						jumpfx.play()
					if dx > 0 :
						self.image = self.images_right[self.index]
						self.direction = 1
					if dx < 0 :
						self.image = self.images_left[self.index]
						self.direction = -1
					if dx == 0:
						if self.direction == 1:
							self.image = self.images_idle_right[self.index]
						if self.direction == -1:
							self.image = self.images_idle_left[self.index]



					if self.counter > walk_cooldown:
						self.counter = 0
						self.index += 1
						if self.index >= len(self.images_right):
							self.index = 0
						
				

					self.rect.x += dx
					self.rect.y += dy
					self.hitbox.x += dx
					self.hitbox.y += dy

					self.control += 1
					self.counter += 1

				else:
					self.ready = True
				screen.blit(self.image, self.rect)
		elif game_over == True:
			if self.death == 0:
				self.index = 0
				self.counter = 0
				self.death = 1
			elif self.death == 1:
				walk_cooldown = 7
				if self.left == True and self.right == False:
					self.image = self.images_die_left[self.index]
				elif self.right == True and self.left == False:
					self.image = self.images_die_right[self.index]
				if self.counter > walk_cooldown:
					self.counter = 0
					self.index += 1
					if self.index >= len(self.images_die_right):
						self.index = 8
					
				self.counter += 1


			

#AFTER GOING TO MAIN MENU BOT FLOATS



#MAP DATA
if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	map_data = pickle.load(pickle_in)
world = World(map_data)

levels_completed = []

def reset_level(level):
	
	fallfx.play()
	if path.exists(f'level{level}_data'):
		pickle_in = open(f'level{level}_data', 'rb')
		map_data = pickle.load(pickle_in)
	world = World(map_data)
	return world

spawnx = world.spawnpoint[0][0]
spawny = world.spawnpoint[0][1]
botspawnx = world.botspawnpoint[0][0]
botspawny = world.botspawnpoint[0][1]
player = Player(spawnx,spawny)
bot = Bot(botspawnx,botspawny)
level_select = False

exit_img2 = pygame.transform.scale(exit_img,(100,50))
restartmainmenu = pygame.image.load('Pictures/RESTART.png')
restartmainmenu = pygame.transform.scale(restartmainmenu,(300,350))
restartpause = Button(screen_width - 370, -197, restartmainmenu)
options = pygame.image.load('Pictures/options.png')
options = pygame.transform.scale(options,(70,70))
optionsbutton = Button(screen_width - 80, 20, options)

#create buttons
restart_button = Button(screen_width // 2 - 50, screen_height//2, restart_img)
start_button = Button(screen_width//2 - 350, screen_height//2 , start_img)
exit_button = Button(screen_width//2 , screen_height//2 , exit_img)
pause_button = Button(screen_width - 60, 20, pause_img)
pauseexit_button = Button(screen_width - 170, 20 , exit_img2)
index = 0
counter = 0
max_levels = 10
running = True
buttonimg = pygame.image.load('Pictures/button.png')
tutorial = pygame.image.load('Pictures/tutorial.png')
mainmenubutton = pygame.image.load('Pictures/mainmenubutton.png')
mainmenubutton = pygame.transform.scale(mainmenubutton,(60,60))
pausemainmenu = Button(screen_width - 70, 80, mainmenubutton)
tutorial.set_colorkey(white)
optionsopen = False
back = pygame.image.load('Pictures/back.png')
back = pygame.transform.scale(back,(70,70))
backbutton = Button(20,30, back)
mainmenusprites = []

songfx = pygame.mixer.Sound('Pictures/song.mp3')
songfx.set_volume(.3)
songfx.play(-1)
guy = pygame.image.load('Pictures/guy.png')
trophyguy = pygame.image.load('Pictures/trophyguy.png')
guy = pygame.transform.scale(guy,(500,500))
trophyguy = pygame.transform.scale(trophyguy,(500,500))
soundicon = pygame.image.load('Pictures/soundon.png')
soundmute = pygame.image.load('Pictures/mute.png')
soundicon = pygame.transform.scale(soundicon,(70,70))
soundmute = pygame.transform.scale(soundmute,(70,70))
soundbutton = Button(100,30,soundicon)
guy_rect = Rect(640,screen_height-250,100,200)
mute = False
secretlevel = False
stilltouch = False
dissapear = False
trophy = False
trophyicon = pygame.image.load('Pictures/trophy.png')

dialogue = ['u finly mad it to the end', 'uhhhhh good job', 'you did it', 'you should probably do something else','um i still think you did a good job?','thumbs up','could you stand on that button and THEN talk to me?']
dialoguefont = pygame.font.Font('Pictures/Peepo.ttf', 20)
textdialogue = dialoguefont.render('', False, (0,0,0))
while running:
	screen.blit(sky,(0,0))
	if trophy == True:
		if main_menu == True:
			screen.blit(trophyicon,(screen_width-150,screen_height-150))

	if level == 11:
		if main_menu == False:
			if trophy == False:
				screen.blit(guy,(500,screen_height - 300))
			elif trophy == True:
				screen.blit(trophyguy,(500,screen_height-300))
			if win1 == False and win2 == False:
				if guy_rect.colliderect(player.hitbox.x,player.hitbox.y,player.width,player.height):
					if stilltouch == False:
						hm = randint(0,6)
						textdialogue = dialoguefont.render(dialogue[hm], False, (0,0,0))
						
						stilltouch = True
				else:
					stilltouch = False
				screen.blit(textdialogue, (470, 700))
			elif win1 == True and win2 == False:
				if guy_rect.colliderect(player.hitbox.x,player.hitbox.y,player.width,player.height):
					if switch == True:
						textdialogue = dialoguefont.render('woah thanks for stepping on that switch heres a trophy!', False, (0,0,0))
						trophy = True
				screen.blit(textdialogue, (300, 700))

	

	if main_menu == True and level_select == False and optionsopen == False:
		
		text_surface = my_font.render("Slime of Time", False, (0,0,0))
		walk_cooldown = 4
		screen.blit(main_menu_slime[index], (screen_width//2 -350, screen_height//2 -650))
		screen.blit(text_surface, (screen_width//2 - 170, screen_height//2 - 300))
		if counter > walk_cooldown:
				counter = 0
				index += 1
				if index >= len(main_menu_slime):
					index = 0
		counter += 1

		if exit_button.draw():
			running = False
		if start_button.draw():
			level_select = True
		if optionsbutton.draw():
			optionsopen = True


	if optionsopen == True:

		if soundbutton.draw():
			if mute == False:
				mute = True
				songfx.stop()
				
			elif mute == True:
				songfx.play(-1)
				mute = False


	if mute == True and optionsopen == True:
		screen.blit(soundmute, (100,30))


	if main_menu == True and (level_select == True or optionsopen == True):
		if backbutton.draw():
			level_select = False
			optionsopen = False



	if level_select == True:
		walk_cooldown = 4
		text_surface = my_font.render("Level Selection", False, (0,0,0))
		screen.blit(text_surface, (screen_width//2 - 180, 50))
		screen.blit(main_menu_slime2[index], (screen_width//2 -250, screen_height - 650))
		screen.blit(main_menu_slime[index], (screen_width//2 -450, screen_height - 650))


		
	



		button1 = Button(150,150,buttonimg)
		if button1.draw():
			level = 1
			world = reset_level(level)
			level_select = False
			main_menu = False
			spawnx = world.spawnpoint[0][0]
			spawny = world.spawnpoint[0][1]
			botspawnx = world.botspawnpoint[0][0]
			botspawny = world.botspawnpoint[0][1]
			player.reset(spawnx, spawny)
			bot.reset(botspawnx, botspawny)
		button2 = Button(300,150,buttonimg)
		if button2.draw():
			level = 2
			world = reset_level(level)
			level_select = False
			main_menu = False
			spawnx = world.spawnpoint[0][0]
			spawny = world.spawnpoint[0][1]
			botspawnx = world.botspawnpoint[0][0]
			botspawny = world.botspawnpoint[0][1]
			player.reset(spawnx, spawny)
			bot.reset(botspawnx, botspawny)
		button3 = Button(450,150,buttonimg)
		if button3.draw():
			level = 3
			world = reset_level(level)
			level_select = False
			main_menu = False
			spawnx = world.spawnpoint[0][0]
			spawny = world.spawnpoint[0][1]
			botspawnx = world.botspawnpoint[0][0]
			botspawny = world.botspawnpoint[0][1]
			player.reset(spawnx, spawny)
			bot.reset(botspawnx, botspawny)
		button4 = Button(600,150,buttonimg)
		if button4.draw():
			level = 4
			world = reset_level(level)
			level_select = False
			main_menu = False
			spawnx = world.spawnpoint[0][0]
			spawny = world.spawnpoint[0][1]
			botspawnx = world.botspawnpoint[0][0]
			botspawny = world.botspawnpoint[0][1]
			player.reset(spawnx, spawny)
			bot.reset(botspawnx, botspawny)
		button5 = Button(750,150,buttonimg)
		if button5.draw():
			level = 5
			world = reset_level(level)
			level_select = False
			main_menu = False
			spawnx = world.spawnpoint[0][0]
			spawny = world.spawnpoint[0][1]
			botspawnx = world.botspawnpoint[0][0]
			botspawny = world.botspawnpoint[0][1]
			player.reset(spawnx, spawny)
			bot.reset(botspawnx, botspawny)
		button6 = Button(150,300,buttonimg)
		if button6.draw():
			level = 6
			world = reset_level(level)
			level_select = False
			main_menu = False
			spawnx = world.spawnpoint[0][0]
			spawny = world.spawnpoint[0][1]
			botspawnx = world.botspawnpoint[0][0]
			botspawny = world.botspawnpoint[0][1]
			player.reset(spawnx, spawny)
			bot.reset(botspawnx, botspawny)
		button7 = Button(300,300,buttonimg)
		if button7.draw():
			level = 7
			world = reset_level(level)
			level_select = False
			main_menu = False
			spawnx = world.spawnpoint[0][0]
			spawny = world.spawnpoint[0][1]
			botspawnx = world.botspawnpoint[0][0]
			botspawny = world.botspawnpoint[0][1]
			player.reset(spawnx, spawny)
			bot.reset(botspawnx, botspawny)
		button8 = Button(450,300,buttonimg)
		if button8.draw():
			level = 8
			world = reset_level(level)
			level_select = False
			main_menu = False
			spawnx = world.spawnpoint[0][0]
			spawny = world.spawnpoint[0][1]
			botspawnx = world.botspawnpoint[0][0]
			botspawny = world.botspawnpoint[0][1]
			player.reset(spawnx, spawny)
			bot.reset(botspawnx, botspawny)
		button9 = Button(600,300,buttonimg)
		if button9.draw():
			level = 9
			world = reset_level(level)
			level_select = False
			main_menu = False
			spawnx = world.spawnpoint[0][0]
			spawny = world.spawnpoint[0][1]
			botspawnx = world.botspawnpoint[0][0]
			botspawny = world.botspawnpoint[0][1]
			player.reset(spawnx, spawny)
			bot.reset(botspawnx, botspawny)
		button10 = Button(750,300,buttonimg)
		if button10.draw():
			level = 10
			world = reset_level(level)
			level_select = False
			main_menu = False
			spawnx = world.spawnpoint[0][0]
			spawny = world.spawnpoint[0][1]
			botspawnx = world.botspawnpoint[0][0]
			botspawny = world.botspawnpoint[0][1]
			player.reset(spawnx, spawny)
			bot.reset(botspawnx, botspawny)
		button11 = Button(450,450,buttonimg)
		



		text_surface = my_font.render("1", False, (0,0,0))
		screen.blit(text_surface, (190, 155))
		text_surface = my_font.render("2", False, (0,0,0))
		screen.blit(text_surface, (339, 155))
		text_surface = my_font.render("3", False, (0,0,0))
		screen.blit(text_surface, (487, 155))
		text_surface = my_font.render("4", False, (0,0,0))
		screen.blit(text_surface, (635, 155))
		text_surface = my_font.render("5", False, (0,0,0))
		screen.blit(text_surface, (790, 155))
		text_surface = my_font.render("6", False, (0,0,0))
		screen.blit(text_surface, (190, 305))
		text_surface = my_font.render("7", False, (0,0,0))
		screen.blit(text_surface, (339, 305))
		text_surface = my_font.render("8", False, (0,0,0))
		screen.blit(text_surface, (487, 305))
		text_surface = my_font.render("9", False, (0,0,0))
		screen.blit(text_surface, (639, 305))
		text_surface = my_font.render("10", False, (0,0,0))
		screen.blit(text_surface, (780, 305))

		if secretlevel == True:


			if button11.draw():
				level = 11
				world = reset_level(level)
				level_select = False
				main_menu = False
				spawnx = world.spawnpoint[0][0]
				spawny = world.spawnpoint[0][1]
				botspawnx = world.botspawnpoint[0][0]
				botspawny = world.botspawnpoint[0][1]
				player.reset(spawnx, spawny)
				bot.reset(botspawnx, botspawny)
				dissapear = True
				level_select = False
				main_menu = False
				
			text_surface = my_font.render("69", False, (0,0,0))
			screen.blit(text_surface, (475, 455))


		if counter > walk_cooldown:
			counter = 0
			index += 1
			if index >= len(main_menu_slime):
				index = 0
		counter += 1


	if main_menu == False:
		clock.tick(60)
		world.draw()

			


		
		if game_over == False:
			if pause_button.draw():
				if pause_menu == True:
					pause_menu = False
				elif pause_menu == False:
					pause_menu = True
						
			if pause_menu == True:
				if pauseexit_button.draw(): 
					running = False
				if restartpause.draw():
					player.movements = []
					player.reset(spawnx, spawny)
					bot.reset(botspawnx,botspawny)
					win1 = False
					win2 = False
					game_over = False
				if pausemainmenu.draw():

					

					player.movements = []
					pause_menu = False
					game_over = False
					main_menu = True
					win1 = False
					win2 = False



		game_over = player.update(game_over)
		bot.update(game_over)



		


		if game_over == True:
			if restart_button.draw():
				player.movements = []
				player.reset(spawnx, spawny)
				bot.reset(botspawnx,botspawny)

				spawn = False
				game_over = False
		if level == 1:
			screen.blit(tutorial,(0,0))






		if win2 == True:
			if level not in levels_completed:
				levels_completed.append(level)
			level += 1

			
			
			

			if level <= max_levels:
				
				
				#SPAWNX + SPAWNY HERE
				
				map_data = []
				world = reset_level(level)

				spawnx = world.spawnpoint[0][0]
				spawny = world.spawnpoint[0][1]
				botspawnx = world.botspawnpoint[0][0]
				botspawny = world.botspawnpoint[0][1]
				player.reset(spawnx, spawny)
				bot.reset(botspawnx,botspawny)
				
				win1 = False
				win2 = False
			elif level > max_levels:
				level = max_levels
				if restart_button.draw():
					
					level = 1
					#reset level
					map_data = []

					
					world = reset_level(level)
					spawnx = world.spawnpoint[0][0]
					spawny = world.spawnpoint[0][1]
					botspawnx = world.botspawnpoint[0][0]
					botspawny = world.botspawnpoint[0][1]	
					player.reset(spawnx, spawny)
					bot.reset(botspawnx, botspawny)
					game_over = 0
					win1 = False
					win2 = False
					level_select = True
					main_menu = True
			
			
	if len(levels_completed) == 10:
		secretlevel = True




	for event in pygame.event.get():


		if event.type == pygame.QUIT:
			running = False

	pygame.display.update()
	
