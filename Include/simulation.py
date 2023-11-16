# Ariel Morandy - first try at python! Jan 2023
from declaration import *
import declaration as d
import pygame
from pygame.locals import *

import classes as c
import method as m
import userinterface as ui


def gameupdate(game, camera):
	side = "Above"
	for machine in d.machine_list:
		# check every target to see if cargos have arrived
		objectfound_list = []
		objectfound_list = m.find_cargo_from_machine(side, machine)

		if isinstance(machine, c.Trash):
			for objectfound in objectfound_list:
				if objectfound != None:
					d.cargo_list.remove(objectfound)
					pygame.sprite.Sprite.kill(objectfound)
					'''game.score = game.score + 1
					print("Score is ", game.score)'''
		elif isinstance(machine, c.Target):
			for objectfound in objectfound_list:
				if objectfound != None:
					# we must check the dna is correct
					if objectfound.moveable == True:
						if objectfound.code_dna == machine.target_dna :
							game.score = game.score + 1
							print("Score is ", game.score)

					# we remove the cargo from the list.
						d.cargo_list.remove(objectfound)
						pygame.sprite.Sprite.kill(objectfound)


		# check every transformer to see if cargos have arrived, and if the transformer is "Empty"
		# transformer follows 3 states
		# 1/Empty : the machine awaits cargo (until all inputs are filled)
		# 2/Processing : the machine proccess for N iterations and releases its cargo (until all outputs are filled)
		# 3/Delivering : the result is ready to be moved (the machine is considered "empty" only when all cargos have cleared the machine)
		elif isinstance(machine, c.Transformer):
			if machine.processing == "Empty":

				for objectfound in objectfound_list:

					if objectfound != None:
						# hide the cargo sprite , and flag the cargo has "in Transformer so that it cannot move)
						pygame.sprite.Sprite.kill(objectfound)

						if isinstance(machine, c.Cutter )  or \
						   isinstance(machine, c.Rotator) or \
						   isinstance(machine, c.Sorter ) :

							machine.cargo_in_1 = objectfound
							machine.processing = "Processing"
							objectfound.in_transformer = True
							print("The machine ",machine, "is now processing")

						if isinstance(machine, c.Assembler) or \
						   isinstance(machine, c.Painter):
							#assembler and Painter load in two steps, because they have two In connnectors
							xtmp,ytmp = m.get_center_from_object (objectfound)
							cnx_name= ""
							cnx_name = machine.get_connector_in(xtmp,ytmp, True, "Above", cnx_name)

							if cnx_name == "Face_L1":
								machine.cargo_in_1 = objectfound
								objectfound.in_transformer = True
							if cnx_name == "Face_L2":
								machine.cargo_in_2 = objectfound
								objectfound.in_transformer = True

							if machine.cargo_in_1 != None and machine.cargo_in_2 != None:
								machine.processing = "Processing"
								print("The machine is now processing", machine)

			elif machine.processing == "Processing":
				machine.iteration_index = machine.iteration_index + 1

				# the transformer has finished
				if machine.iteration_index == machine.iteration:

					machine.processing = "Delivering"

					if isinstance(machine, c.Cutter):
						print("Entering Cutter transformer")
						code_out_left, code_out_right = m.shape_vertical_cut(machine.cargo_in_1.code_dna)

						# create two half shapes cargos if they are not empty.
						if code_out_left != empty_shape_dna:
							cnx_type, cnx_state, x, y, delta_col, delta_row = m.get_connector_from_name(machine,"Face_R1")
							# we position the new cargo on the Transformer tile
							x = x - tile_size // 2 * delta_col
							y = y - tile_size // 2 * delta_row
							col_left, row_left = m.get_colrow_from_coordinates(x, y)

							# create cargo
							cargo_left = c.Custom_shape(col_left, row_left, machine.angle)
							#we need to position the x,y of the cargo on the top-left tile
							cargo_left.x, cargo_left.y = col_left*tile_size, row_left*tile_size

							cargo_left.generate(code_out_left)
							cargo_left.offset(camera.offsetx, camera.offsety)
							d.cargo_list.append(cargo_left)
							d.all_sprites_cargos_list.add(cargo_left)
							machine.cargo_out_1 = cargo_left

						if code_out_right != empty_shape_dna:
							cnx_type, cnx_state, x, y, delta_col, delta_row = m.get_connector_from_name(machine, "Face_R2")
							# we position the new cargo on the Transformer tile
							x = x - tile_size // 2 * delta_col
							y = y - tile_size // 2 * delta_row
							col_right, row_right = m.get_colrow_from_coordinates(x, y)

							#create cargo
							cargo_right = c.Custom_shape(col_right, row_right, machine.angle)
							#we need to position the x,y of the cargo on the top-left tile
							cargo_right.x, cargo_right.y = col_right*tile_size, row_right*tile_size

							cargo_right.generate(code_out_right)
							cargo_right.offset(camera.offsetx, camera.offsety)
							d.cargo_list.append(cargo_right)
							d.all_sprites_cargos_list.add(cargo_right)
							machine.cargo_out_2 = cargo_right

						# finally we remove the old cargo.
						d.cargo_list.remove(machine.cargo_in_1)
						machine.cargo_in_1 = None
						print("we create two cargos")

					if isinstance(machine, c.Rotator):
						print ("Entering rotation transformer")
						cargo = machine.cargo_in_1
						new_code_dna = m.shape_rotate (cargo.code_dna,machine.rotation_angle)
						cargo.generate(new_code_dna)
						cargo.offset(camera.offsetx, camera.offsety)

						machine.cargo_in_1 = None
						print("we rotated the cargo")
						machine.cargo_out_1 = cargo
						# we show again the sprite and free the cargo
						d.all_sprites_cargos_list.add(cargo)
						cargo.in_transformer = False

					if isinstance(machine, c.Assembler):
						print("Entering Assembler transformer")
						cargo1 = machine.cargo_in_1
						cargo2 = machine.cargo_in_2
						new_code_dna = m.shape_assemble (cargo1.code_dna,cargo2.code_dna)

						#we create a new cargo
						cargo= c.Custom_shape(cargo1.col,cargo1.row, machine.angle)
						cargo.x , cargo.y = cargo1.col * tile_size,cargo1.row * tile_size

						d.cargo_list.append(cargo)
						cargo.generate(new_code_dna)
						cargo.offset(camera.offsetx, camera.offsety)

						#we clean the inputs, and set the ouput
						machine.cargo_in_1 = None
						machine.cargo_in_2 = None
						print("we assembled the cargo")
						machine.cargo_out_1 = cargo

						# we show again the sprite and delete the cargos
						d.all_sprites_cargos_list.add(cargo)

						pygame.sprite.Sprite.kill(cargo1)
						pygame.sprite.Sprite.kill(cargo2)
						d.cargo_list.remove(cargo1)
						d.cargo_list.remove(cargo2)

					if isinstance(machine, c.Sorter):
						print("Entering Sorter")
						# we show again the sprite and free the cargo
						cargo = machine.cargo_in_1
						machine.cargo_in_1 = None
						d.all_sprites_cargos_list.add(cargo)
						cargo.in_transformer = False

						#we check the filter, default is going to the "Cnx_False"
						for dna in machine.dna_code_filter:
							'''if cargo.code_dna == dna [0] and dna [2] <dna [1]:'''
							if cargo.code_dna == dna [0] :
								dna [2] = dna [2] +1
								machine.T[1][3] = True
								machine.T[2][3] = False
								print ("Cargo is selected")
							else:
								machine.T[1][3] = False
								machine.T[2][3] = True
								print ("Cargo is not selected")

					if isinstance(machine, c.Painter):
						print("Entering Painter transformer")
						cargo_shape = machine.cargo_in_1
						cargo_color = machine.cargo_in_2

						#we change the color
						cargo_shape.code_dna = m.shape_color(cargo_shape.code_dna, cargo_color.color)

						#we regenerate the shape , and release from transformer
						cargo_shape.generate(cargo_shape.code_dna)
						cargo_shape.offset(camera.offsetx, camera.offsety)
						cargo_shape.in_transformer = False

						#we clean the inputs, and set the ouput
						machine.cargo_in_1 = None
						machine.cargo_in_2 = None
						print("we painted  the cargo")
						machine.cargo_out_1 = cargo_shape

						# we show again the sprite and delete the cargo carrying the color
						d.all_sprites_cargos_list.add(cargo_shape)
						pygame.sprite.Sprite.kill(cargo_color)

						d.cargo_list.remove(cargo_color)


	for cargo in d.cargo_list:
		# check if a cargo needs to move in the right direction.
		# cargo moves at its own speed
		#we only move cargos which are not inside a transformer
		if cargo.move == False and cargo.in_transformer == False:

			# check on which machine the cargo is
			x,y = m.get_center_from_object(cargo)
			machine_start = m.find_machine_from_coord(x,y)

			# we calculate the next position of cargo , and the next machine.
			machine_end,vector_col,vector_row,newside, gomove = move_cargo (cargo,machine_start)

			# all goes well, we can move the cargo, else we exit.
			if gomove:
				# the current cargo can be moved
				# we initialize the speed of the cargo.

				cargo.delta_x = vector_col / cargo.step
				cargo.delta_y = vector_row / cargo.step
				cargo.col = cargo.col + vector_col
				cargo.row = cargo.row + vector_row
				cargo.move = True
				cargo.angle = machine_end.angle
				cargo.rotate()
				# we register the cargo on the correct side of the Tunnel.
				cargo.tunnel_side = newside

				# if the machine start has several outputs, we switched to the next one
				if isinstance(machine_start, c.Splitter):
					machine_start.alternate_output()

				# if the machine end has several inputs, we switched to the next one
				if isinstance(machine_start, c.Merger):
					machine_start.alternate_input()

				# if the machine is a Transformer, and if the cargo was the last to depart, we put the machine on "Empty""
				if      ((isinstance(machine_start, c.Cutter   ))  and machine_start.processing == "Delivering") or \
						((isinstance(machine_start, c.Rotator  ))  and machine_start.processing == "Delivering") or \
						((isinstance(machine_start, c.Assembler))  and machine_start.processing == "Delivering") or \
						((isinstance(machine_start, c.Painter  ))  and machine_start.processing == "Delivering") or \
						((isinstance(machine_start, c.Sorter   ))  and machine_start.processing == "Delivering"):
					# clean the outputs
					if machine_start.cargo_out_1 == cargo:
						machine_start.cargo_out_1 = None
					if machine_start.cargo_out_2 == cargo:
						machine_start.cargo_out_2 = None
					# the machine has completed the job when all output are None
					if machine_start.cargo_out_1 == None and machine_start.cargo_out_2 == None :
						machine_start.iteration_index = 0
						machine_start.processing = "Empty"


	for machine in d.machine_list:
		# check every source if a cargo needs to be created, if the source is ready to deliver one cargo
		if isinstance(machine, c.Source):
			# increment every source operation index by 1
			machine.iteration_index = machine.iteration_index + 1
			if machine.iteration_index == machine.iteration:
				machine.iteration_index = 0
				objectfound = None
				#this method could be changed for find_cargo_from_machine
				objectfound = m.find_cargo("Above", machine.col, machine.row)
				if objectfound == None:
					cargo = eval("c." + machine.delivery)(machine.col, machine.row, machine.angle)

					if isinstance(cargo,c.Custom_shape):
					# generate shape one time
						cargo.generate(machine.code_dna)

					if isinstance(cargo,c.Custom_color):
					# generate color one time
						cargo.generate(machine.color)

					# and place it at the correct location, using the cmaera offset.
					cargo.offset (camera.offsetx,camera.offsety)

					d.cargo_list.append(cargo)
					d.all_sprites_cargos_list.add(cargo)
					'''print("we create one cargo")'''

def move_cargo (cargo, machine_start):

	machine_end = None
	tunnel_case = False
	side = ""
	newside = "Above"
	gomove = False

	x, y, vector_col, vector_row = 0, 0, 0, 0

	if machine_start != None:

		side_start = cargo.tunnel_side

		#general cases
		if  isinstance(machine_start, c.Conveyor)    or \
			isinstance(machine_start, c.Elbow_left)  or \
		    isinstance(machine_start, c.Elbow_right) or \
			isinstance(machine_start, c.Merger)      or \
			isinstance(machine_start, c.Source)      or \
			isinstance(machine_start, c.Transformer) or \
			isinstance(machine_start, c.Tunnel):

			# we get the nearest connector out
			xtmp,ytmp = cargo.x+tile_size//2,cargo.y+tile_size//2
			cnx_closest =""
			cnx_closest = machine_start.get_connector_out(xtmp, ytmp, True, side_start, cnx_closest)

			# we look for a connected part
			for relation in d.relationship_list:
				# what are the relationship between this machine and the others
				if machine_start == relation[2]:
					# one relationship found to the IN of a machine
					cnx_name = relation[3]
					machine_end = relation[0]
					'''print("relation to", machine_end, "which has a connector name", relation[1])'''

					if isinstance(machine_end, c.Transformer) and machine_end.processing !="Empty":
						vector_col, vector_row, newside = 0,0,"Above"
						return machine_end, vector_col, vector_row, newside, gomove

					if relation[4] !="Any":
						#cwe must check that the cargo can go to this machine, excluding color or shape
						if isinstance(cargo,c.Custom_shape) and relation[4] !="Shape":
							return machine_end, vector_col, vector_row, newside, gomove
						elif isinstance(cargo,c.Custom_color) and relation[4] !="Color":
							return machine_end, vector_col, vector_row, newside, gomove

					if cnx_name == cnx_closest:
						#we found a connector
						cnx_type = ""
						cnx_state = False
						'''x, y, vector_col, vector_row = 0, 0, 0, 0'''
						cnx_type, cnx_state, x, y, vector_col, vector_row = m.get_connector_from_name(machine_start,cnx_name)

						tunnel_break = False
						if isinstance(machine_start, c.Tunnel):
							if (cargo.tunnel_side == "Above" and cnx_name != "Face_R"):
								tunnel_break = True
							elif (cargo.tunnel_side == "Below" and cnx_name != "Face_T"):
								tunnel_break = True

						if tunnel_break == False:
							# special case, the cargo is arriving on a tunnel, we must determine which side. Default is "Above"
							if isinstance(machine_end, c.Tunnel):
								newside = m.get_tunnel_side(machine_start.col, machine_start.row, machine_end,
								                            newside)
							else:
								newside = "Above"

						# calculate the position of adjacent point
						xadj = x + tile_size // 2 * vector_col
						yadj = y + tile_size // 2 * vector_row

						adjcol, adjrow = m.get_colrow_from_coordinates(xadj, yadj)

						#we must use the Col and Row method and not coord because cargo are not there "yet"
						adjcargofound = None
						adjcargofound = m.find_cargo(newside, adjcol, adjrow)
						if adjcargofound == None:
							'''print("no cargo found we can move it")'''
							gomove = True
							return machine_end, vector_col, vector_row, newside, gomove

		# specific cases
		elif  isinstance(machine_start, c.Splitter):
			#we get the  connector out

			# 1/we start with True connector
			xtmp,ytmp = m.get_center_from_object(cargo)
			cnx_name =""
			cnx_name = machine_start.get_connector_out(xtmp, ytmp, True, side_start, cnx_name)

			# we look for a connected part
			machine_end, cnx_name2, rel_type, result = m.get_rel(machine_start, cnx_name)

			if result:
				# we get the connector position.
				cnx_type, cnx_state, x, y, vector_col, vector_row = m.get_connector_from_name(machine_start,cnx_name)


				# calculate the position of adjacent point
				xadj = x + tile_size // 2 * vector_col
				yadj = y + tile_size // 2 * vector_row

				adjcol, adjrow = m.get_colrow_from_coordinates(xadj, yadj)

				#we must use the Col and Row method and not coord because cargo are not there "yet"
				adjcargofound = None
				adjcargofound = m.find_cargo(newside, adjcol, adjrow)
				if adjcargofound == None:
					print("Splitter case : True connector found")
					gomove = True
					return machine_end, vector_col, vector_row, newside, gomove


			# 2/Failed : we look with FALSE connector
			'''xtmp, ytmp = cargo.rect.centerx, cargo.rect.centery'''
			cnx_name = ""
			cnx_name = machine_start.get_connector_out(xtmp, ytmp, False, side_start, cnx_name)

			# we look for a connected part
			machine_end, cnx_name2, rel_type,result2 = m.get_rel(machine_start, cnx_name)

			if result2:
				# we get the connector position.
				x, y, vector_col, vector_row = 0, 0, 0, 0
				cnx_type = ""
				cnx_state = False
				cnx_type, cnx_state, x, y, vector_col, vector_row = m.get_connector_from_name(machine_start,cnx_name)

				# calculate the position of adjacent point
				xadj = x + tile_size // 2 * vector_col
				yadj = y + tile_size // 2 * vector_row

				adjcol, adjrow = m.get_colrow_from_coordinates(xadj, yadj)

				# we must use the Col and Row method and not coord because cargo are not there "yet"
				adjcargofound = None
				adjcargofound = m.find_cargo(newside, adjcol, adjrow)
				if adjcargofound == None:
					print("Splitter case : True connector found")
					gomove = True
					return machine_end, vector_col, vector_row, newside, gomove



	return machine_end,vector_col,vector_row,newside, gomove


