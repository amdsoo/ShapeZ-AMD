import math
import pygame
from pygame.locals import *
from declaration import *
import declaration as d
import method as m
from array import *
import pickle as pick
import os

pygame.font.init()

# basic font for user typed
my_font = pygame.font.SysFont('Comic Sans MS', 30)
# small font for user typed
my_font_S = pygame.font.SysFont('Comic Sans MS', 12)


class World():
	def __init__(self):
		self.tile_list = []
		# load images
		grey_img = pygame.image.load('img/grey.png')
		colmax = screen_width // tile_size
		rowmax = screen_height// tile_size
		col_count = 0

		while col_count < colmax:
			# top level
			img = pygame.transform.scale(grey_img, (tile_size, tile_size))
			img_rect = img.get_rect()
			img_rect.x = col_count * tile_size
			img_rect.y = 0
			tile = (img, img_rect)
			self.tile_list.append(tile)

			# lowlevel
			img = pygame.transform.scale(grey_img, (tile_size, tile_size))
			img = pygame.transform.rotate(img, 180)
			img_rect = img.get_rect()
			img_rect.x = col_count * tile_size
			img_rect.y = rowmax* tile_size - tile_size
			tile = (img, img_rect)
			self.tile_list.append(tile)

			col_count +=1

	def draw(self, screen):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])


class Game():
	def __init__(self):
		self.score = 0
		self.state = "Stop"
		# number of iterations between two game update (no machine shoud run faster than this)
		self.iteration = 10
		# tracking game update trigger
		self.iteration_index = 0
		self.target_cargo = None

	def draw(self, screen):
		# create rectangle
		input_rect = pygame.Rect(tile_size, 0, 4 * tile_size, tile_size)
		pygame.draw.rect(screen, GREY, input_rect)
		text_surface = my_font.render("Score is / " + str(self.score), False, BLACK)
		screen.blit(text_surface, (input_rect.x + 5, 0))

	def get_tile_info (self,col,row):
		newline = ":"
		#we write the coordinates
		long_message = "Col/" + str(col) + " - " + "Row/" + str(row)+ newline
		x=col*tile_size+tile_size//2
		y=row*tile_size+tile_size//2
		long_message =  long_message + "x center/" + str(x) + " - " + "y center/" + str(y) + newline


		#we try to find the machine or cargo on the tile
		machine = None
		machine = m.find_machine(col, row)
		if machine != None:
			long_message = long_message+ "Machine/"+ str(type(machine))+ newline

		cargo = None
		cargo = m.find_cargo("Above",col, row)
		if cargo != None:
			long_message = long_message+ "Cargo-Above/"+ str(type(cargo))+ newline

		cargo = None
		cargo = m.find_cargo("Below",col, row)
		if cargo != None:
			long_message = long_message+ "Cargo-Below/"+ str(type(cargo))+ newline

		return long_message

	def draw_msg (self,screen,msg):
		newline = ":"
		lines = msg.split(newline)
		i=0
		for line in lines:
			text_surface = my_font_S.render(line, True, WHITE)
			screen.blit(text_surface, (screen_width-5*tile_size, screen_height-4*tile_size+i*15))
			i=i+1

	def save_game(self, camera):
		# this is the save sequence.
		# open a file, where  to store the data
		file = open('savefolder/save_game_file_new', 'wb')

		#deserialize the sprites
		for machine in d.machine_list:
			machine.image = None
			machine.image_org = None

		for cargo in d.cargo_list:
			cargo.image     = None
			cargo.image_org = None

		self.target_cargo.image = None
		self.target_cargo.image_org = None


		# dump information to that file
		pickle_list =[]
		pickle_list.append(camera)
		pickle_list.append(d.machine_list)
		pickle_list.append(d.relationship_list)
		pickle_list.append(d.all_sprites_machines_list)
		pickle_list.append(d.cargo_list)
		pickle_list.append(d.all_sprites_cargos_list)
		pickle_list.append(self.target_cargo)
		pick.dump(pickle_list   , file)

		# close the file
		file.close()
		pygame.quit()

	def open_game(self, camera):
		# this is the Open game sequence.
		print ("Clear the game")
		# first we must reset the actual game.
		d.all_sprites_cargos_list.empty()
		d.all_sprites_machines_list.empty()
		d.cargo_list.clear()
		d.machine_list.clear()
		d.relationship_list.clear()
		self.iteration_index = 0
		self.score = 0

		# second,open a file amd pickle the data
		file = open('savefolder/save_game_file_new', 'rb')

		pickle_list           = pick.load(file)
		camera                = pickle_list[0]
		d.machine_list        = pickle_list[1]
		d.relationship_list   = pickle_list[2]
		d.all_sprites_machines_list = pickle_list[3]
		d.cargo_list          = pickle_list[4]
		d.all_sprites_cargos_list = pickle_list[5]
		target_cargo       = pickle_list[6]
		self.target_cargo = target_cargo


		# we restore the sprites
		for machine in d.machine_list:
			machine.image = pygame.transform.rotate(pygame.image.load(machine.image_name), machine.angle)

		for cargo in d.cargo_list:
			if isinstance(cargo,Custom_shape):
				cargo.generate(cargo.code_dna)
			else:
				cargo.generate(cargo.color)
			cargo.image_org = cargo.image
			cargo.offset(camera.offsetx, camera.offsety)

		target_cargo.generate(target_cargo.code_dna)
		target_cargo.image_org = target_cargo.image
		target_cargo.offset(camera.offsetx, camera.offsety)

		print("Game Reloaded")

		return camera


class Grid():
	def __init__(self):
		pass

	def draw (self, screen, camera):
		horiz  =  world_height // tile_size + 1
		vertic =  world_width  // tile_size + 1

		h, v = 0, 0
		offsetx=camera.offsetx
		offsety= camera.offsety
		delta_row = offsety // tile_size
		delta_col = offsetx // tile_size

		test_indent = 9

		i = 0
		for line in range(0, horiz):
			pygame.draw.line(screen, (255, 255, 255), (0 - offsetx, line * tile_size - offsety),
			                 (screen_width, line * tile_size - offsety))
			# Write Text (Col,Row) and Screen/World Coordinates
			if i > 0:
				'''text = "(" + str(delta_col) + "," + str(delta_row + i + 1) + ")"'''
				text = str(delta_row + i + 1) + ")"
				text_surface = my_font_S.render(text, True, WHITE)
				screen.blit(text_surface, (test_indent, tile_size * i + tile_size))
			i = i + 1

		i = 0
		for line in range(0, vertic):
			pygame.draw.line(screen, (255, 255, 255), (line * tile_size - offsetx, -offsety),
			                 (line * tile_size - offsetx, screen_height))
			# Write Text (Col,Row) and Screen/World Coordinates
			'''text = "(" + str(delta_col + i) + "," + str(delta_row + 1) + ")"'''
			text = "(" + str(delta_col + i) +  ")"
			text_surface = my_font_S.render(text, True, WHITE)
			screen.blit(text_surface, (tile_size * i + test_indent, tile_size))
			i = i + 1


class Camera():
	def __init__(self,offsetx,offsety):
		self.offsetx = offsetx
		self.offsety = offsety


class Machine(pygame.sprite.Sprite):
	def __init__(self, camera , col, row, angle):
		super().__init__()
		# ------------------------
		# size 1: one CELL
		#      T
		#   L[ X ] R
		#      B
		# ------------------------
		# size 2: 2 CELLS vertical
		#      T
		# L1 [ X ] R1
		# L2 [ X ] R2
		#      B
		# ------------------------
		# size 4: 4 CELLS in square
		#      T1   T2
		# L1 [ X ][ X ] R1
		# L2 [ X ][ X ] R2
		#      B1   B2

		self.size = 1
		self.row = row
		self.col = col
		self.x = self.col * tile_size
		self.y = self.row * tile_size
		self.angle = angle
		img = pygame.transform.scale(tmp_img, (tile_size, tile_size))
		self.image_org = pygame.transform.rotate(img, 0)
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.image_name = path_tmp
		#we intialize the sprite base on camera position
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		# Connector table
		# Machine can be 1 cell, 2 cells or 4 cells, connectors are stated for each side of the cell
		# [ 0, 3 ]
		# [ 1, 2 ]
		# Connector table , connectors are stated in the referential of the Machine [Name,x,y,"Type",Flag open, x, y ]
		self.T = ["Cnx_xxx", "Face_test", "Out", False, 0, 0]

	def rotate(self):
		self.angle = self.angle + 90
		if self.angle == 360:
			self.angle = 0
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()

	def set_connectors_coord (self):
		i = 0
		for connector in self.T:
			connector_type, connector_state, x, y, col, row = "", False, 0, 0, 0, 0
			connector_type, connector_state, x, y, col, row = m.get_connector_from_name(self,connector[1])
			print("Connector ", connector[0], connector[1], "coord x/", x, "coord y/", y, "col/", col, "row/", row)

			# ["Cnx_in_1", "Face_L", "In", True, 0, 0]
			self.T[i][4] = x
			self.T[i][5] = y
			i = i + 1

	def get_connector_out(self, x0, y0,state,side,connector_name):
		# return a connector name  OUT, for a given State, or the closest to x0, y0
		# migrated

		connector_name = "None"

		# Cutter case /we look for the closest connector, the state or side is not important
		if isinstance(self, Cutter):
			d = 1000.
			for connector in self.T:
				if connector[2] == "Out":
					dtest = math.sqrt(math.pow(connector[4] - x0, 2) + math.pow(connector[5] - y0, 2))
					if dtest < d:
						# we found a smaller distance
						connector_name = connector[1]
						d = dtest

		# Tunnel Cases (to be removed later)
		elif isinstance(self, Tunnel):
			if side == "Above":
				connector_name = "Face_R"
			elif side == "Below":
				connector_name = "Face_T"
		else:
			# all the others cases, we take the first connector out for a given state.
			for connector in self.T:
				if connector[2] == "Out" and connector[3] == state:
					connector_name = connector[1]

		return connector_name

	def get_connector_in (self, x0, y0,state,side,connector_name):
		# return a connector name  IN, for a given State, or the closest to x0, y0
		# migrated

		connector_name = "None"

		# Assembler and painter case /we look for the closest connector, the state or side is not important
		if isinstance(self, Assembler) or isinstance(self, Painter):
			d = tile_size*10
			for connector in self.T:
				if connector[2] == "In":
					dtest = math.sqrt(math.pow(connector[4] - x0, 2) + math.pow(connector[5] - y0, 2))
					if dtest < d:
						# we found a smaller distance
						connector_name = connector[1]
						d = dtest

		# Tunnel Cases (to be removed later)
		elif isinstance(self, Tunnel):
			if side == "Above":
				connector_name = "Face_L"
			elif side == "Below":
				connector_name = "Face_B"
		else:
			# all the others cases, we take the first connector In for a given state.
			for connector in self.T:
				if connector[2] == "In" and connector[3] == state:
					connector_name = connector[1]

		return connector_name

	def get_connector_in_at_coord(self, x, y, connector_name):
		# provides the connector name that corresponds to the x, y coordinates in  input
		col = 0
		row = 0
		xtmp = 0
		ytmp = 0
		cnx_type = ""
		cnx_state = True
		connector_name = ""

		# check Face R
		cnx_type, cnx_state, xtmp, ytmp, col, row = m.get_connector_from_name(self, "Face_R")
		if x == xtmp and y == ytmp and cnx_type == "In" and cnx_state == True:
			connector_name = "Face_R"
		# check Face T
		cnx_type, cnx_state, xtmp, ytmp, col, row = m.get_connector_from_name(self, "Face_T")
		if x == xtmp and y == ytmp and cnx_type == "In" and cnx_state == True:
			connector_name = "Face_T"
		# check Face L
		cnx_type, cnx_state, xtmp, ytmp, col, row = m.get_connector_from_name(self, "Face_L")
		if x == xtmp and y == ytmp and cnx_type == "In" and cnx_state == True:
			connector_name = "Face_L"
		# check Face B
		cnx_type, cnx_state, xtmp, ytmp, col, row = m.get_connector_from_name(self, "Face_B")
		if x == xtmp and y == ytmp and cnx_type == "In" and cnx_state == True:
			connector_name = "Face_B"

		return connector_name

	def get_connector_name_at_coord(self, x, y):
		# provides the connector name that corresponds to the x, y coordinates in  input
		# this method checks the exact match (not closest)
		col = 0
		row = 0
		xtmp = 0
		ytmp = 0
		cnx_type = ""
		cnx_state = True
		connector_name = ""
		connector_type = ""

		# check Face R
		cnx_type, cnx_state, xtmp, ytmp, col, row = m.get_connector_from_name(self, "Face_R")
		if x == xtmp and y == ytmp:
			connector_name = "Face_R"
			connector_type = cnx_type
			return connector_name, connector_type

		# check Face T
		cnx_type, cnx_state, xtmp, ytmp, col, row = m.get_connector_from_name(self, "Face_T")
		if x == xtmp and y == ytmp:
			connector_name = "Face_T"
			connector_type = cnx_type
			return connector_name, connector_type

		# check Face L
		cnx_type, cnx_state, xtmp, ytmp, col, row = m.get_connector_from_name(self, "Face_L")
		if x == xtmp and y == ytmp:
			connector_name = "Face_L"
			connector_type = cnx_type
			return connector_name, connector_type

		# check Face B
		cnx_type, cnx_state, xtmp, ytmp, col, row = m.get_connector_from_name(self, "Face_B")
		if x == xtmp and y == ytmp:
			connector_name = "Face_B"
			connector_type = cnx_type
			return connector_name, connector_type

		# check Face B
		cnx_type, cnx_state, xtmp, ytmp, col, row = m.get_connector_from_name(self, "Face_L1")
		if x == xtmp and y == ytmp:
			connector_name = "Face_L1"
			connector_type = cnx_type
			return connector_name, connector_type

		# check Face B
		cnx_type, cnx_state, xtmp, ytmp, col, row = m.get_connector_from_name(self, "Face_L2")
		if x == xtmp and y == ytmp:
			connector_name = "Face_L2"
			connector_type = cnx_type
			return connector_name, connector_type

		# check Face B
		cnx_type, cnx_state, xtmp, ytmp, col, row = m.get_connector_from_name(self, "Face_R1")
		if x == xtmp and y == ytmp:
			connector_name = "Face_R1"
			connector_type = cnx_type
			return connector_name, connector_type

		# check Face B
		cnx_type, cnx_state, xtmp, ytmp, col, row = m.get_connector_from_name(self, "Face_R2")
		if x == xtmp and y == ytmp:
			connector_name = "Face_R2"
			connector_type = cnx_type
			return connector_name, connector_type

		return connector_name, connector_type

	def draw_connectors(self, screen, camera):
		# method migrated
		for connector in self.T:
			machine2 = None
			cnx_name2 = ""
			result = False
			# we draw only unconnected connector
			machine2, cnx_name2, rel_type, result = m.get_rel(self,connector[1])

			if result == False:

				#in world coordinates
				cnx_type, cnx_state, x, y, col, row = m.get_connector_from_name(self,connector[1])

				# color choice
				if connector[2] == "Out":
					color = RED
					size = tile_size // 10
				elif connector[2] == "In":
					color = WHITE
					size = tile_size // 5

				# we draw the circles (we must go in screen coordinates
				pos = x -camera.offsetx, y-camera.offsety
				output_1 = pygame.draw.circle(screen, color, pos, size, 2)

	def offset (self,offsetx,offsety):
		self.rect.x = self.rect.x - offsetx
		self.rect.y = self.rect.y - offsety


class Conveyor(Machine):
	def __init__(self, camera , col, row, angle):
		Machine.__init__(self, camera, col, row, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(cv_img, (tile_size, tile_size))
		self.angle = angle
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.image_name = path_cv
		self.rect = self.image.get_rect()
		#we intialize the sprite base on camera position
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		# Connector table : position Name/positionx,y/Type/Open or Close
		# this position never changes for rotation.
		self.T = [
			["Cnx_in_1", "Face_L", "In", True, 0, 0],
			["Cnx_out_1", "Face_R", "Out", True, 0, 0]
		]


class Elbow_right(Machine):
	def __init__(self, camera , col, row, angle):
		Machine.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(elb_right_img, (tile_size, tile_size))
		self.angle = angle
		self.image_name = path_elb_right_img
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		# Connector table

		self.T = [
			["Cnx_in_1", "Face_L", "In", True, 0, 0],
			["Cnx_out_1", "Face_B", "Out", True, 0, 0]
		]


class Elbow_left(Machine):
	def __init__(self, camera , col, row, angle):
		Machine.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(elb_left_img, (tile_size, tile_size))
		self.angle = angle
		self.image_name = path_elb_left_img
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		# Connector table
		self.T = [
			["Cnx_in_1", "Face_L", "In", True, 0, 0],
			["Cnx_out_1", "Face_T", "Out", True, 0, 0]
		]


class Splitter(Machine):
	def __init__(self, camera , col, row, angle):
		Machine.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(tmp_img, (tile_size, tile_size))
		self.angle = angle
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

	def alternate_output(self):
		if self.T[1][3]:
			self.T[1][3] = False
			self.T[2][3] = True
		else:
			self.T[1][3] = True
			self.T[2][3] = False


class Splitter_right(Splitter):
	def __init__(self, camera , col, row, angle):
		Splitter.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(splitter_right_img, (tile_size, tile_size))
		self.angle = angle
		self.image_name = path_splitter_right_img
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		# Connector table
		# 2 possibilities for output (R= Right, L = Left, B = Bootm, U = Up)
		# two outputs on the right side at angle =0, and one on the bottom side

		self.T = [
			["Cnx_in_1", "Face_L", "In", True, 0, 0],
			["Cnx_out_1", "Face_R", "Out", True, 0, 0],
			["Cnx_out_2", "Face_B", "Out", False, 0, 0]
		]


class Splitter_left(Splitter):
	def __init__(self, camera , col, row, angle):
		Splitter.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(splitter_left_img, (tile_size, tile_size))
		self.angle = angle
		self.image_name = path_splitter_left_img
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		# Connector table
		# 2 possibilities for output (R= Right, L = Left, B = Bootm, U = Up)
		# two outputs on the right side at angle =0, and one on the bottom side

		self.T = [
			["Cnx_in_1" , "Face_L", "In" , True , 0, 0],
			["Cnx_out_1", "Face_R", "Out", True , 0, 0],
			["Cnx_out_2", "Face_T", "Out", False, 0, 0]
		]


class Merger(Machine):
	def __init__(self, camera , col, row, angle):
		Machine.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(tmp_img, (tile_size, tile_size))
		self.angle = angle
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety


	def alternate_input(self):
		#ugly need to be migrated

			if self.T[0][3] == True:
				self.T[0][3] = False
				self.T[2][3] = True
			else:
				self.T[0][3] = True
				self.T[2][3] = False


class Merger_right(Merger):
	def __init__(self, camera , col, row, angle):
		Merger.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(merger_right_img, (tile_size, tile_size))
		self.angle = angle
		self.image_name = path_merger_right_img
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		# Connector table

		self.T = [
			["Cnx_in_1" , "Face_L", "In" , True , 0, 0],
			["Cnx_out_1", "Face_R", "Out", True , 0, 0],
			["Cnx_in_2" , "Face_B", "In" , False, 0, 0]
		]


class Merger_left(Merger):
	def __init__(self, camera , col, row, angle):
		Merger.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(merger_left_img, (tile_size, tile_size))
		self.angle = angle
		self.image_name = path_merger_left_img
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		# Connector table

		self.T = [
			["Cnx_in_1" , "Face_L", "In" , True , 0, 0],
			["Cnx_out_1", "Face_R", "Out", True , 0, 0],
			["Cnx_in_2" , "Face_T", "In" , False, 0, 0]
		]


class Tunnel(Machine):
	def __init__(self, camera , col, row, angle):
		Machine.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(cv_tunnel_img, (tile_size, tile_size))
		self.angle = angle
		self.image_name = path_cv_tunnel_img
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		# Connector table
		self.T = [
			["Cnx_out_1", "Face_R", "Out", True, 0, 0],
			["Cnx_out_2", "Face_T", "Out", True, 0, 0],
			["Cnx_in_1", "Face_L", "In", True, 0, 0],
			["Cnx_in_2", "Face_B", "In", True, 0, 0]
		]

		# specific to Tunnel who have two sides
		self.connector_in_below  = "Face_B"
		self.connector_out_below = "Face_T"
		self.connector_in_above  = "Face_L"
		self.connector_out_above = "Face_R"


class Target(Machine):
	def __init__(self, camera , col, row, angle):
		Machine.__init__(self, camera , col, row, angle)
		self.size = 1
		self.delivery = "Custom_shape"
		#a random dna is computed at creation.
		self.target_dna = ""
		self.target_score  = 100
		self.current_score = 0

		# Connector table
		self.T = [
			["Cnx_in_1", "Face_R", "In", True, 0, 0],
			["Cnx_in_3", "Face_L", "In", True, 0, 0]
				]


class Target_x1(Target):
	def __init__(self, camera, col, row, angle):
		Target.__init__(self, camera, col, row, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(target_img, (tile_size, tile_size))
		self.angle = angle
		self.image_name = path_target_img
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety


		# Connector table
		self.T = [
			["Cnx_in_1", "Face_R", "In", True, 0, 0],
			["Cnx_in_3", "Face_L", "In", True, 0, 0]
		]

class Trash (Machine):
	def __init__(self, camera , col, row, angle):
		Machine.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_name = path_trash_img
		img = pygame.transform.scale(trash_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(img, 0)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		# Connector table
		self.T = [
			["Cnx_in_1", "Face_R", "In", True, 0, 0],
			["Cnx_in_2", "Face_T", "In", True, 0, 0],
			["Cnx_in_3", "Face_L", "In", True, 0, 0],
			["Cnx_in_4", "Face_B", "In", True, 0, 0]
		]

class Source(Machine):
	def __init__(self, camera , col, row, angle):
		Machine.__init__(self, camera , col, row, angle)
		self.size = 1
		self.angle = angle

		# number of iterations between two operations
		self.iteration = 20
		# tracking game update trigger
		self.iteration_index = 0

		# Connector table
		# Possibilities for output (R= Right, L = Left, B = Bootm, U = Up)
		# 1 outputs on the right side at angle =0, and one on the bottom side
		self.T = [
			["Cnx_out_1", "Face_R", "Out", True, 0, 0]
		]


class Sqr_plate_deliver(Source):
	def __init__(self, camera , col, row, angle):
		Source.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_name = path_src_square_plate_deliver_img
		self.image_org = pygame.transform.scale(src_square_plate_deliver_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety
		self.delivery = "Custom_shape"
		'''self.code_dna = "S1g/n/n/n/n:S1d/n/n/n/n:C1g/n/n/n/n:T1r/n/n/n/n&" \
		                "S2b/n/n/n/n:C2r/n/n/n/n:C2b/n/n/n/n:T2r/n/n/n/n"'''
		self.code_dna = "S1d/n/n/n/n:S1d/n/n/n/n:S1d/n/n/n/n:S1d/n/n/n/n"
		self.iteration = 10


class Cir_plate_deliver(Source):
	def __init__(self, camera , col, row, angle):
		Source.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_name = path_src_circle_plate_deliver_img
		self.image_org = pygame.transform.scale(src_circle_plate_deliver_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety
		self.delivery = "Custom_shape"
		self.code_dna = "C1d/n/n/n/n:C1d/n/n/n/n:C1d/n/n/n/n:C1d/n/n/n/n"
		self.iteration = 20


class Tri_plate_deliver(Source):
	def __init__(self, camera , col, row, angle):
		Source.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_name = path_src_triangle_plate_deliver_img
		self.image_org = pygame.transform.scale(src_triangle_plate_deliver_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety
		self.delivery = "Custom_shape"
		self.code_dna = "T1d/n/n/n/n:T1d/n/n/n/n:T1d/n/n/n/n:T1d/n/n/n/n"
		self.iteration = 30


class Color_deliver(Source):
	def __init__(self, camera , col, row, angle):
		Source.__init__(self, camera , col, row, angle)
		self.size = 1
		self.image_name = path_tmp
		self.image_org = pygame.transform.scale(tmp_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety
		self.color = GREY
		self.iteration = 10


class Red_paint_deliver(Color_deliver):
	def __init__(self, camera , col, row, angle):
		Color_deliver.__init__(self, camera , col, row, angle)
		self.image_name = path_red_paint_deliver_img
		self.image_org = pygame.transform.scale(red_paint_deliver_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.color = RED
		self.delivery = "Custom_color"


class Blue_paint_deliver(Color_deliver):
	def __init__(self, camera , col, row, angle):
		Color_deliver.__init__(self, camera , col, row, angle)
		self.image_name = path_blue_paint_deliver_img
		self.image_org = pygame.transform.scale(blue_paint_deliver_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.color = BLUE
		self.delivery = "Custom_color"


class Green_paint_deliver(Color_deliver):
	def __init__(self, camera , col, row, angle):
		Color_deliver.__init__(self, camera , col, row, angle)
		self.image_name = path_green_paint_deliver_img
		self.image_org = pygame.transform.scale(green_paint_deliver_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.color = GREEN
		self.delivery = "Custom_color"


class Transformer(Machine):
	def __init__(self, camera , col, row, angle):
		Machine.__init__(self, camera , col, row, angle)

		# temporary image to initiate rect.
		self.image_org = pygame.transform.scale(cv_img, (tile_size, tile_size))
		self.angle = angle
		self.size = 2

		# transformer follows 3 states
		# 1/Empty : the machine awaits cargo
		# 2/Processing : the machine proccess for N iterations
		# 3/Delivering : the result is ready to be moved

		self.processing = "Empty"

		# how many cycles to process
		self.iteration = 15
		self.iteration_index = 0

		#management of inputs /those are Objects not, DNA
		self.cargo_in_number =0
		self.cargo_in_1 = None
		self.cargo_in_2 = None

		#management of Output /Those are Objects not, DNA
		self.cargo_out_number = 0
		self.cargo_out_1 = None
		self.cargo_out_2 = None

		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		# Connector table
		# transformer can be 1 cell, 2 cells or 4 cells, connectors are stated for each side of the cell
		#      T
		# L1 [ A ] R1
		# L2 [ B ] R2
		#      B
		self.size = 2
		self.T = [["Cnx_tst" , "Face_test", "None" , True, 0, 0]]


class Cutter(Transformer):
	def __init__(self, camera , col, row, angle):
		Transformer.__init__(self, camera , col, row, angle)
		self.image_name = path_cutter_obj_img
		self.image_org = pygame.transform.scale(cutter_obj_img, (tile_size, 2 * tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.size = 2
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		self.delivery = "Custom_shape"

		# how many cycles to process
		self.iteration = 1

		self.cargo_in_number = 1
		self.cargo_in_1 = None
		self.cargo_in_2 = None

		# management of Output /Those are Objects not, DNA
		self.cargo_out_number = 2
		self.cargo_out_1 = None
		self.cargo_out_2 = None

		self.T = [
				["Cnx_in_1" , "Face_L1", "In" , True, 0, 0],
				["Cnx_out_1", "Face_R1", "Out", True, 0, 0],
				["Cnx_out_2", "Face_R2", "Out", True, 0, 0]
				 ]


class Rotator (Transformer):
	def __init__(self, camera , col, row, angle):
		Transformer.__init__(self, camera , col, row, angle)
		self.image_org = pygame.transform.scale(rotator_ccw_obj_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.size = 1
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		self.delivery = "Custom_shape"

		#three possible angles / 90/180/270
		self.rotation_angle = 90

		# how many cycles to process
		self.iteration = 5

		self.cargo_in_number = 1
		self.cargo_in_1 = None
		self.cargo_in_2 = None

		# management of Output /Those are Objects not, DNA
		self.cargo_out_number = 1
		self.cargo_out_1 = None
		self.cargo_out_2 = None

		self.T = [
				["Cnx_in_1" , "Face_L", "In" , True, 0, 0],
				["Cnx_out_1", "Face_R", "Out", True, 0, 0],
				 ]


class Rotator_ccw (Rotator):
	def __init__(self, camera , col, row, angle):
		Rotator.__init__(self, camera , col, row, angle)
		self.image_name = path_rotator_ccw_obj_img
		self.image_org = pygame.transform.scale(rotator_ccw_obj_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.size = 1
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		self.delivery = "Custom_shape"
		#three possible angles / 90/180/270 (270 corresponds to (-90)
		self.rotation_angle = 90

		# how many cycles to process
		self.iteration = 5


class Assembler (Transformer):
	def __init__(self, camera , col, row, angle):
		Transformer.__init__(self, camera , col, row, angle)
		self.image_name = path_assembler_obj_img
		self.image_org = pygame.transform.scale(assembler_obj_img, (tile_size, 2 *tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.size = 2
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		self.delivery = "Custom_shape"


		# how many cycles to process
		self.iteration = 1

		self.cargo_in_number = 2
		self.cargo_in_1 = None
		self.cargo_in_2 = None

		# management of Output /Those are Objects not, DNA
		self.cargo_out_number = 1
		self.cargo_out_1 = None
		self.cargo_out_2 = None

		self.T = [
				["Cnx_in_1" , "Face_L1", "In" , True, 0, 0],
				["Cnx_in_2" , "Face_L2", "In" , True, 0, 0],
				["Cnx_out_1", "Face_R1", "Out", True, 0, 0],
				 ]


class Sorter (Transformer):
	def __init__(self, camera , col, row, angle):
		Transformer.__init__(self, camera , col, row, angle)
		self.image_name = path_sorter_img
		self.image_org = pygame.transform.scale(sorter_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.size = 1
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety


		# List of dna_code the command can filter
		# format is ["dna code", number of expected cargo, number of realized cargo]
		# "?" is wild card.
		self.dna_code_filter = [
			["S/n/n/n/n:S/n/n/n/n:S/n/n/n/n:S/n/n/n/n",1,0],
								]

		# how many cycles to process
		self.iteration = 5

		# behavior : cargo leaves via "Cnx_True" if condition = True, else "Cnx_False"
		# default is false (this needs to be determined by the simulation, cargo per cargo.
		self.T = [
				["Cnx_in_1" , "Face_L", "In" , True, 0, 0],
				["Cnx_True" , "Face_R", "Out", False, 0, 0],
				["Cnx_False", "Face_B", "Out", True, 0, 0],
				 ]


class Painter(Transformer):
	def __init__(self, camera , col, row, angle):
		Transformer.__init__(self, camera , col, row, angle)
		self.image_name = path_painter_obj_img
		self.image_org = pygame.transform.scale(painter_obj_img, (tile_size, 2 * tile_size))
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.size = 2
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size - camera.offsetx
		self.rect.y = self.row * tile_size - camera.offsety

		self.delivery = "Custom_shape"

		# how many cycles to process
		self.iteration = 5

		self.cargo_in_number = 2
		self.cargo_in_1 = None
		self.cargo_in_2 = None

		# management of Output /Those are Objects not, DNA
		self.cargo_out_number = 1
		self.cargo_out_1 = None
		self.cargo_out_2 = None

		self.T = [
				["Cnx_in_1" , "Face_L1", "In" , True, 0, 0],
				["Cnx_in_2" , "Face_L2", "In" , True, 0, 0],
				["Cnx_out_1", "Face_R1", "Out", True, 0, 0]
				 ]


class Cargo(pygame.sprite.Sprite):
	def __init__(self, col, row, angle):
		super().__init__()

		self.row = row
		self.col = col

		self.x = self.col * tile_size
		self.y = self.row * tile_size

		# default dna shape
		self.code_dna = ""
		self.in_transformer = False

		# angle to position the sprite, not the physical angle
		self.angle = angle

		# managing animation
		self.moveable = True
		self.move = False
		self.step = 10
		self.move_index = 0
		self.delta_x = 0
		self.delta_y = 0

		# tunnel case , the cargo can be im a tunnel , Above or Below
		self.tunnel = None
		self.tunnel_side = "Above"

	def update(self):
		# the cargo moves and when it reaches its destination, the next move must be recomputed
		if self.move:
			self.rect.x = self.rect.x + self.delta_x * tile_size
			self.rect.y = self.rect.y + self.delta_y * tile_size
			self.move_index = self.move_index + 1
		if self.move_index == self.step:
			self.move_index = 0
			self.move = False
			# now we can set the proper W coordinates
			self.x = self.col * tile_size
			self.y = self.row * tile_size

	def rotate(self):
		self.image = pygame.transform.rotate(self.image_org, self.angle)

	def offset(self, offsetx, offsety):
		self.rect.x = self.rect.x - offsetx
		self.rect.y = self.rect.y - offsety


class Custom_shape(Cargo):
	def __init__(self, col, row, angle):
		Cargo.__init__(self, col, row, angle)

		# this angle is to control the sprite display. it doesnt affect the quadrants.
		self.angle = angle
		self.color = RUSTY

		# Quadrant Template [Type(S,T,C,H,N)/VertexFeature(r,s,n)/Position of Quadrant (x,y)]
		# quadrant [0]   = type (string)   / base shape for the quadrant
		#                  - S = Square, T = Triangle, C = Circle , H = Hyperbolic , N = No Draw
		# quadrant [1,4] = feature (string /quadrant feature, 4 values, corresponding to the 4 points X (axis X), O (opposite), Y (Axis Y), C (Center)
		#                  - "r" = Round, "s" = snipe or "n" = No Draw
		# quadrant [5]   = (x,y) (Tuple)   / Position of Quadrant (x,y)


	def generate(self, code_dna):
		# the method encode dna om a custom shape, from a formatted string "code"
		# for instance "S1d/s/s/s/s:R1g/n/r/s/s:N0d/n/n/n/n:C3y/s/s/n/n"
		self.code_dna = code_dna

		#how many layers
		layers = code_dna.split("&")

		# create original support to project all quadrants
		image_shape = pygame.Surface([2 * qz, 2 * qz])
		image_shape.fill(BLACK)

		layer_num = 0

		for layer in layers:

		# get each quadrant
			quadrant_list = layer.split(":")
			q0 = quadrant_list[0].split("/")
			q1 = quadrant_list[1].split("/")
			q2 = quadrant_list[2].split("/")
			q3 = quadrant_list[3].split("/")

			# preparation of points coordinates based on size of each quadrant
			pt_c = []
			pt_x = []
			pt_o = []
			pt_y = []
			size_q =[]
			pos_q = []

			#get the size of each quadrant
			size_q.append(quadrant_size [q0[0][1:2]])
			size_q.append(quadrant_size [q1[0][1:2]])
			size_q.append(quadrant_size [q2[0][1:2]])
			size_q.append(quadrant_size [q3[0][1:2]])

			# for Q0
			tmp_pt_c = (0, qz)
			tmp_pt_x = (size_q[0], qz)
			tmp_pt_o = (size_q[0], qz-size_q[0])
			tmp_pt_y = (0, qz-size_q[0])
			pt_c.append(tmp_pt_c)
			pt_x.append(tmp_pt_x)
			pt_o.append(tmp_pt_o)
			pt_y.append(tmp_pt_y)
			pos_q.append((qz,0))

			# for Q1
			tmp_pt_c = (qz, qz)
			tmp_pt_x = (qz-size_q[1], qz)
			tmp_pt_o = (qz-size_q[1], qz-size_q[1])
			tmp_pt_y = (qz, qz-size_q[1])
			pt_c.append(tmp_pt_c)
			pt_x.append(tmp_pt_x)
			pt_o.append(tmp_pt_o)
			pt_y.append(tmp_pt_y)
			pos_q.append((0, 0))

			# for Q2
			tmp_pt_c = (qz, 0)
			tmp_pt_x = (qz-size_q[2], 0)
			tmp_pt_o = (qz-size_q[2], size_q[2])
			tmp_pt_y = (qz, size_q[2])
			pt_c.append(tmp_pt_c)
			pt_x.append(tmp_pt_x)
			pt_o.append(tmp_pt_o)
			pt_y.append(tmp_pt_y)
			pos_q.append((0, qz))

			# for Q3
			tmp_pt_c = (0, 0)
			tmp_pt_x = (size_q[3], 0)
			tmp_pt_o = (size_q[3], size_q[3])
			tmp_pt_y = (0, size_q[3])
			pt_c.append(tmp_pt_c)
			pt_x.append(tmp_pt_x)
			pt_o.append(tmp_pt_o)
			pt_y.append(tmp_pt_y)
			pos_q.append((qz, qz))

			draw = False
			i = 0

			for quadrant in quadrant_list:
				#we draw only if size is >0
				if size_q [i]!=0:
					# create a temporary surface to draw each quadrant
					image_quadrant = pygame.Surface([qz, qz])
					image_quadrant.fill(BLACK)
					color = m.get_color_from_string (quadrant)

					# 1/we draw the  Quadrant
					if quadrant[0][0:1] == "S":
						# Draw Quadrant
						print("Quadrant #", i, "is  RECT")
						if i==0:
							pygame.draw.rect(image_quadrant, color, pygame.Rect(pt_y[i],pt_x[i]))
							pygame.draw.rect(image_quadrant, DARKSHADE, pygame.Rect(pt_y[i], pt_x[i]),1)
						elif i==1:
							pygame.draw.rect(image_quadrant, color, pygame.Rect(pt_o[i],pt_c[i]))
							pygame.draw.rect(image_quadrant, DARKSHADE, pygame.Rect(pt_o[i],pt_c[i]),1)
						elif i==2:
							pygame.draw.rect(image_quadrant, color, pygame.Rect(pt_x[i],pt_y[i]))
							pygame.draw.rect(image_quadrant, DARKSHADE, pygame.Rect(pt_x[i], pt_y[i]),1)
						elif i==3:
							pygame.draw.rect(image_quadrant, color, pygame.Rect(pt_c[i],pt_o[i]))
							pygame.draw.rect(image_quadrant, DARKSHADE, pygame.Rect(pt_c[i], pt_o[i]),1)
						draw = True
					elif quadrant[0][0:1]  == "C":
						print("Quadrant #", i, "is  CIRC")
						if i == 0:
							pygame.draw.circle(image_quadrant, color, pt_c[i], size_q[i], draw_top_right=True)
							pygame.draw.circle(image_quadrant, DARKSHADE, pt_c[i], size_q[i], draw_top_right=True,width=1)
						elif i == 1:
							pygame.draw.circle(image_quadrant, color, pt_c[i], size_q[i], draw_top_left=True)
							pygame.draw.circle(image_quadrant, DARKSHADE, pt_c[i], size_q[i], draw_top_left=True,width=1)
						elif i == 2:
							pygame.draw.circle(image_quadrant, color, pt_c[i], size_q[i], draw_bottom_left=True)
							pygame.draw.circle(image_quadrant, DARKSHADE, pt_c[i], size_q[i], draw_bottom_left=True,width=1)
						elif i == 3:
							pygame.draw.circle(image_quadrant, color, pt_c[i], size_q[i], draw_bottom_right=True)
							pygame.draw.circle(image_quadrant, DARKSHADE, pt_c[i], size_q[i], draw_bottom_right=True,width=1)
						draw = True
					elif quadrant[0][0:1]  == "T":
						print("Quadrant #", i, "is  TRIANGLE")
						pygame.draw.polygon(image_quadrant, color, [pt_c[i], pt_x[i], pt_y[i]])
						pygame.draw.polygon(image_quadrant, DARKSHADE, [pt_c[i], pt_x[i], pt_y[i]],width=1)
						draw = True
					else:
						print("Quadrant #", i, "is  not drawn")
						draw = False

					if draw:
						# 2/we draw the features of the Quadrant /4 points X (axis X), O (opposite), Y (Axis Y), C (Center)
						'''if quadrant[1] == "r":
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
							                     (xcenter, ycenter + ss)])'''

						# 3/we can now draw the quadrant onto the main surface
						image_quadrant.set_colorkey(BLACK)
						image_shape.blit(image_quadrant, pos_q[i])
						draw = False

				i = i + 1

		# we create two lines in black to separate the quadrants
		pygame.draw.line(image_shape, BLACK, (qz, 0), (qz, 2 * qz))
		pygame.draw.line(image_shape, BLACK, (0, qz), (2 * qz, qz))

		'''image_shape.set_colorkey(BLACK)'''

		self.image = image_shape
		self.image_org = image_shape
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size + tile_size // 10
		self.rect.y = self.row * tile_size + tile_size // 10


class Custom_color(Cargo):
	def __init__(self, col, row, angle):
		Cargo.__init__(self, col, row, angle)
		self.color = WHITE

	def generate (self,color):

		self.color = color

		if color == RED:
			self.image_name = path_red_paint_obj_img
			self.image_org = pygame.transform.scale(red_paint_obj_img, (tile_size*0.8, tile_size*0.8))
		elif color == GREEN:
			self.image_name = path_green_paint_obj_img
			self.image_org = pygame.transform.scale(green_paint_obj_img, (tile_size*0.8, tile_size*0.8))
		elif color == BLUE:
			self.image_name = path_blue_paint_obj_img
			self.image_org = pygame.transform.scale(blue_paint_obj_img, (tile_size*0.8, tile_size*0.8))

		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.col * tile_size + tile_size // 10
		self.rect.y = self.row * tile_size + tile_size // 10


