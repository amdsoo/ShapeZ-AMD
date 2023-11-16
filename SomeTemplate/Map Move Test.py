import pygame
from pygame.locals import *



shape_size = 100
quadrant_size = shape_size/2
qz= quadrant_size
snipe_ratio = 4
#snipes sizes
sr = qz/snipe_ratio
ss = qz/snipe_ratio

deltax= 0
deltay= 0

tile_size = 50
screen_width = 1600
screen_height = 1000

world_width = 3200
world_height = 1600

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (220,220,220)
LIGHTSHADE = (170, 170, 170)
DARKSHADE = (100, 100, 100)
RUSTY = (99, 11, 27)

#mouse click index
LEFT = 1
RIGHT = 3


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))

tmp_img = pygame.image.load('img/cutter_obj.png')

class Camera():
	def __init__(self,offsetx,offsety):
		self.offsetx = 0
		self.offsety = 0

def grid_draw(screen,offsetx,offsety):
	horiz  = 2*screen_height//tile_size +1
	vertic = 2*screen_width //tile_size +1

	h,v =0,0

	for line in range(0, horiz):
		pygame.draw.line(screen, (255, 255, 255), (0-offsetx, line * tile_size-offsety), (screen_width, line * tile_size-offsety))

	for line in range(0, vertic):
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size-offsetx, -offsety), (line * tile_size-offsetx, screen_height))

class Machine (pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()

		self.image_org  = pygame.transform.scale(tmp_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(self.image_org, 0)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Cargo(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.angle = 90

		#create original support
		image_shape = pygame.Surface([shape_size, shape_size])

		#first quadrant Q0
		image_q0 = pygame.Surface([quadrant_size, quadrant_size])
		print ("draw a RECT")
		pygame.draw.rect(image_q0 , RED, pygame.Rect(0 ,0, quadrant_size, quadrant_size))
		pygame.draw.circle(image_q0 ,BLACK,(0,0), quadrant_size/snipe_ratio)

		image_shape.blit(image_q0,(quadrant_size,0))


		self.image = image_shape
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def offset (self,offsetx,offsety):
		self.rect.x = self.rect.x - offsetx
		self.rect.y = self.rect.y - offsety


camera = Camera (0,0)

# This is a list of every sprite. For Cargos
all_sprites_cargos_list = pygame.sprite.Group()


cargo = Cargo (250,250)
all_sprites_cargos_list.add(cargo)
cargo = Cargo (0,0)
all_sprites_cargos_list.add(cargo)
cargo = Cargo (1500,900)
all_sprites_cargos_list.add(cargo)
cargo = Cargo (3100,1500)
all_sprites_cargos_list.add(cargo)

all_sprites_cargos_list.update(0,0)

# game loop


run = True
while run:
	clock.tick(60)

	for event in pygame.event.get():
		Mouse_x, Mouse_y = pygame.mouse.get_pos()
		if event.type == pygame.QUIT:
			run = False

	if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
		print("we click at screen coord ", Mouse_x, Mouse_y)
		wcoordx = Mouse_x + camera.offsetx
		wcoordy = Mouse_y + camera.offsety
		print ("translated into world coord ",wcoordx, wcoordy)

	if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
		print("Left Arrow button used")
		deltax =  - 8

	if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
		print("Right Arrow button used")
		deltax =  8

	if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
		print("Left Arrow button used")
		deltay =  - 8


	if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
		print("Right Arrow button used")
		deltay =  8

	if camera.offsetx+deltax <= 0:
		deltax = 0
		camera.offsetx = 0
		print ("we reached the limit in X-")

	if camera.offsety+deltay <= 0:
		deltay = 0
		camera.offsety = 0
		print ("we reached the limit in Y-")

	if camera.offsetx+deltax > (world_width-screen_width):
		deltax = 0
		camera.offsetx = world_width-screen_width
		print ("we reached the limit in X+")

	if camera.offsety+deltay > (world_height-screen_height):
		deltay = 0
		camera.offsety =world_height-screen_height
		print("we reached the limit in Y+")

	camera.offsetx = camera.offsetx + deltax
	camera.offsety = camera.offsety + deltay


	# intialisation of world , with machines
	screen.fill(BLACK)

	grid_draw(screen,camera.offsetx,camera.offsety)

	all_sprites_cargos_list.draw(screen)


	'''cargo.offset(deltax,deltay)'''
	for cargo in all_sprites_cargos_list:
		cargo.offset(deltax, deltay)

	all_sprites_cargos_list.update()

	pygame.display.update()

	deltax = 0
	deltay = 0



pygame.quit()
