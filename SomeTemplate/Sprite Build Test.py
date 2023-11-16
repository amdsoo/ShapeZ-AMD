import pygame
from pygame.locals import *
from declaration import *

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


		image_shape.blit(image_q1,(0,0))

		self.image = image_shape
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Generic_shape (pygame.sprite.Sprite):
	def __init__(self, col, row, angle, code_dna):
		super().__init__()

		#this angle is to control the sprite display. it doesnt affect the quadrants.
		self.angle = 0

		self.row = row
		self.col = col

		# Quadrant Template [Type(S,T,C,H,N)/VertexFeature(r,s,n)/Position of Quadrant (x,y)]
		# quadrant [0]   = type (string)   / base shape for the quadrant
		#                  - S = Square, T = Triangle, C = Circle , H = Hyperbolic , N = No Draw
		# quadrant [1,4] = feature (string /quadrant feature, 4 values, corresponding to the 4 points X (axis X), O (opposite), Y (Axis Y), C (Center)
		#                  - "r" = Round, "s" = snipe or "n" = No Draw
		# quadrant [5]   = (x,)) (Tuple)   / Position of Quadrant (x,y)

		code = code_dna
		#get each quadrant
		q= code.split(":")
		q0 = q[0].split("/")
		q1 = q[1].split("/")
		q2 = q[2].split("/")
		q3 = q[3].split("/")

		self.quadrant_desc_list = [
			[q0[0], q0[1], q0[2], q0[3], q0[4], (qz, 0)],
			[q1[0], q1[1], q1[2], q1[3], q1[4], (0, 0)],
			[q2[0], q2[1], q2[2], q2[3], q2[4], (0, qz)],
			[q3[0], q3[1], q3[2], q3[3], q3[4], (qz, qz)]
		]

	def update(self):

		#create original support to project all quadrants
		image_shape = pygame.Surface([shape_size, shape_size])

		#preparation of points coordinates
		pt_c = []
		pt_x = []
		pt_o = []
		pt_y = []
		# for Q0
		tmp_pt_c = (0 ,qz)
		tmp_pt_x = (qz,qz)
		tmp_pt_o = (qz,0 )
		tmp_pt_y = (0 ,0 )
		pt_c.append(tmp_pt_c)
		pt_x.append(tmp_pt_x)
		pt_o.append(tmp_pt_o)
		pt_y.append(tmp_pt_y)

		# for Q1
		tmp_pt_c  = (qz,qz)
		tmp_pt_x  = (0 ,qz)
		tmp_pt_o  = (0 ,0 )
		tmp_pt_y  = (qz,0 )
		pt_c.append(tmp_pt_c)
		pt_x.append(tmp_pt_x)
		pt_o.append(tmp_pt_o)
		pt_y.append(tmp_pt_y)

		# for Q2
		tmp_pt_c  = (qz,0 )
		tmp_pt_x  = (0 ,0 )
		tmp_pt_o  = (0 ,qz)
		tmp_pt_y  = (qz,qz)
		pt_c.append(tmp_pt_c)
		pt_x.append(tmp_pt_x)
		pt_o.append(tmp_pt_o)
		pt_y.append(tmp_pt_y)

		# for Q3
		tmp_pt_c  = (0 ,0 )
		tmp_pt_x  = (qz,0 )
		tmp_pt_o  = (qz,qz)
		tmp_pt_y  = (0 ,qz)
		pt_c.append(tmp_pt_c)
		pt_x.append(tmp_pt_x)
		pt_o.append(tmp_pt_o)
		pt_y.append(tmp_pt_y)

		draw = False
		i= 0

		for quadrant in self.quadrant_desc_list:
			#create a temporary surface to draw each quadrant
			image_quadrant = pygame.Surface([qz, qz])

			#1/we draw the Base Shape of the Quadrant
			if quadrant [0]== "S":
				#Draw Quadrant
				print ("Quadrant #", i, "is  RECT")
				pygame.draw.rect(image_quadrant , RED, pygame.Rect(0 ,0, qz, qz))
				draw = True
			elif quadrant [0] == "C":
				print("Quadrant #", i, "is  CIRC")
				if i==0:
					pygame.draw.circle(image_quadrant, GREEN, pt_c[i], qz, draw_top_right=True)
				elif i==1:
					pygame.draw.circle(image_quadrant, GREEN, pt_c[i], qz, draw_top_left=True)
				elif i==2:
					pygame.draw.circle(image_quadrant, GREEN, pt_c[i], qz, draw_bottom_left=True)
				elif i==3:
					pygame.draw.circle(image_quadrant, GREEN, pt_c[i], qz, draw_bottom_right=True)
				draw = True
			elif quadrant [0]== "T":
				print("Quadrant #", i, "is  TRIANGLE")
				pygame.draw.polygon(image_quadrant, GREY, [pt_c[i], pt_x[i], pt_y[i]])
				draw = True
			else:
				print("Quadrant #", i, "is  not drawn")
				draw = False

			if draw:
				# 2/we draw the features of the Quadrant /4 points X (axis X), O (opposite), Y (Axis Y), C (Center)
				if quadrant[1] == "r":
					pygame.draw.circle(image_quadrant, BLACK, pt_x[i], sr)
				if quadrant[2] == "r":
					pygame.draw.circle(image_quadrant, BLACK, pt_o[i], sr)
				if quadrant[3] == "r":
					pygame.draw.circle(image_quadrant, BLACK, pt_y[i], sr)
				if quadrant[4] == "r":
					pygame.draw.circle(image_quadrant, BLACK, pt_c[i], sr)

				if quadrant[1] == "s":
					xcenter, ycenter = pt_x[i]
					pygame.draw.polygon(image_quadrant, BLACK,
					                    [(xcenter + ss, ycenter), (xcenter, ycenter - ss), (xcenter - ss, ycenter),
					                     (xcenter, ycenter + ss)])
				if quadrant[2] == "s":
					xcenter, ycenter = pt_o[i]
					pygame.draw.polygon(image_quadrant, BLACK,
					                    [(xcenter + ss, ycenter), (xcenter, ycenter - ss), (xcenter - ss, ycenter),
					                     (xcenter, ycenter + ss)])
				if quadrant[3] == "s":
					xcenter, ycenter = pt_y[i]
					pygame.draw.polygon(image_quadrant, BLACK,
					                    [(xcenter + ss, ycenter), (xcenter, ycenter - ss), (xcenter - ss, ycenter),
					                     (xcenter, ycenter + ss)])
				if quadrant[4] == "s":
					xcenter, ycenter = pt_c[i]
					pygame.draw.polygon(image_quadrant, BLACK,
					                    [(xcenter + ss, ycenter), (xcenter, ycenter - ss), (xcenter - ss, ycenter),
					                     (xcenter, ycenter + ss)])

			# 3/we can now draw the quadrant onto the main surface
				image_shape.blit(image_quadrant, quadrant[5])
				draw = False

			i =i+1

		#we create two lines in black to separate the quadrants
		pygame.draw.line(image_shape, BLACK, (qz, 0), (qz, 2*qz))
		pygame.draw.line(image_shape, BLACK, (0 ,qz), (2*qz, qz))

		image_shape.set_colorkey(BLACK)

		self.image = image_shape
		self.rect = self.image.get_rect()
		self.rect.x = self.col
		self.rect.y = self.row

	def encode_dna (self, code_dna):
	#the method encode dna om a custom shape, from a formatted string "code"
	# for instance S/s/s/s/s:R/n/r/s/s:N/n/n/n/n:C/s/s/n/n
		code = code_dna
		#get each quadrant
		q= code.split(":")
		q0 = q[0].split("/")
		q1 = q[1].split("/")
		q2 = q[2].split("/")
		q3 = q[3].split("/")

		self.quadrant_desc_list = [
			[q0[0], q0[1], q0[2], q0[3], q0[4], (qz, 0)],
			[q1[0], q1[1], q1[2], q1[3], q1[4], (0, 0)],
			[q2[0], q2[1], q2[2], q2[3], q2[4], (0, qz)],
			[q3[0], q3[1], q3[2], q3[3], q3[4], (qz, qz)]
		]


# This is a list of every sprite. For Cargos
all_sprites_cargos_list = pygame.sprite.Group()

code_dna = "S/s/s/s/s:N/n/r/s/s:N/n/n/n/n:C/s/s/n/n"
cargo = Generic_shape (100,100, 0,code_dna)
all_sprites_cargos_list.add(cargo)


code_dna = "S/s/s/s/s:N/n/r/s/s:N/n/n/n/n:C/s/s/n/n"
cargo.encode_dna(code_dna)


all_sprites_cargos_list.update()

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
	all_sprites_cargos_list.draw(screen)

	if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
		print("Left Arrow button used")
		offsetx = offsetx - 1

	if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
		print("Right Arrow button used")
		offsetx = offsetx + 1
	# delete the temporary object, remove the sprite


	pygame.display.update()



pygame.quit()
