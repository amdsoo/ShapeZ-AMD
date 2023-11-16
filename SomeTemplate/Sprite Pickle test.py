import pygame
from pygame.locals import *
from declaration import *
import pickle as pick

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))

shape_size = 50
quadrant_size = shape_size/2
qz= quadrant_size
snipe_ratio = 4
#snipes sizes
sr = qz/snipe_ratio
ss = qz/snipe_ratio

tmp_img = pygame.image.load('img/machine.png')

class Machine (pygame.sprite.Sprite):
	def __init__(self, x, y, test):
		super().__init__()
		self.test = test
		image_org  = pygame.transform.scale(tmp_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(image_org, 0)
		self.image_path = 'img/machine.png'
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


# This is a list of every sprite. For Cargos
all_sprites_machines_list = pygame.sprite.Group()
machines_list = []

'''machine_inst1 = Machine (25, 50, "Ariel")
all_sprites_machines_list.add(machine_inst1)
machines_list.append(machine_inst1)

machine_inst2 = Machine (25, 150,"Sophie")
all_sprites_machines_list.add(machine_inst2)
machines_list.append(machine_inst2)'''

all_sprites_machines_list.update()

# game loop
inwork_mode = False
tmp_object = None
tmp_object_angle = 0
placement_type = ""



run = True
while run:
	clock.tick(60)

	for event in pygame.event.get():
		Mouse_x, Mouse_y = pygame.mouse.get_pos()
		if event.type == pygame.QUIT:
			run = False

	# intialisation of world , with machines
	screen.fill(BLACK)
	all_sprites_machines_list.draw(screen)

	if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
		print("Left Arrow button used")
		file = open('savefolder/save_game_file.txt', 'wb')
		'''pygame.image.tostring(machine_inst1.image,"RGB")
		pygame.image.tostring(machine_inst2.image,"RGB")'''
		machine_inst1.image = None
		machine_inst2.image = None
		pick.dump(machines_list, file)
		# close the file
		file.close()
		pygame.quit()



	if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
		print("Right Arrow button used")
		file = open('savefolder/save_game_file.txt', 'rb')

		# dump information to that file
		machines_list = pick.load(file)
		image_org = pygame.transform.scale(tmp_img, (tile_size, tile_size))
		for machine in machines_list:
			machine.image = pygame.transform.rotate(image_org, 0)
			all_sprites_machines_list.add(machine)

		# close the file
		file.close()
	# delete the temporary object, remove the sprite


	pygame.display.update()


pygame.quit()
