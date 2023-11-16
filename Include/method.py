import random
import declaration as d
import classes as c
from declaration import *

# basic font for user typed
pygame.font.init()
my_font_S = pygame.font.SysFont('Comic Sans MS', 12)

def find_machine_from_coord (x , y):
	# Works in W coordinates
	objectfound = None

	for machine in d.machine_list:
		x1_screen,y1_screen = machine.rect.topleft
		x2_screen,y2_screen = machine.rect.bottomright
		dx = x2_screen - x1_screen
		dy = y2_screen - y1_screen

		x1 , y1 = machine.x, machine.y
		x2 , y2 = x1+dx,y1+dy

		if x1 <= x <= x2:
			if y1 <= y <= y2:
				objectfound = machine
	return objectfound


def find_cargo(side, col, row):
	# the method finds cargo at the coordinates' col, row, and return the object if found
	objectfound = None
	for cargo in d.cargo_list:
		if cargo.col == col and cargo.row == row and cargo.tunnel_side == side:
			objectfound = cargo
			return objectfound


def find_cargo_from_coord(side,x,y):
	# Works in W coordinates
	objectfound = None
	d = tile_size/2
	for cargo in d.cargo_list:
		x1_screen,y1_screen = cargo.rect.topleft
		x2_screen,y2_screen = cargo.rect.bottomright
		dx = x2_screen - x1_screen
		dy = y2_screen - y1_screen

		x1 , y1 = cargo.x, cargo.y
		x2 , y2 = x1+dx, y1+dy

		if x1 < x < x2:
			if y1 < y < y2:
				if cargo.tunnel_side == side:
					objectfound = cargo
	return objectfound


def find_cargo_from_machine(side, machine):
	# the method finds cargo at the location of a machine,and return  the object if found
	# a machine can have more than one cargo
	objectfound_list = []
	for cargo in d.cargo_list:
		if machine.size ==1: # code for one cell machine
			if machine.col == cargo.col and machine.row == cargo.row:
				objectfound_list.append(cargo)
		elif machine.size ==2: # code for two cell machine
			if machine.angle ==0 or machine.angle ==180:
				if (machine.col == cargo.col and machine.row == cargo.row) or (machine.col  == cargo.col and machine.row +1 == cargo.row):
					objectfound_list.append(cargo)
			else:
				if (machine.col == cargo.col and machine.row == cargo.row) or (machine.col +1 == cargo.col and machine.row == cargo.row):
					objectfound_list.append(cargo)
	return objectfound_list


def find_machine(col, row):
	# the method finds machine at the coordinates' col, row, and return  the object if found
	# Works in W coordinates
	objectfound = None

	for machine in d.machine_list:
		if machine.size == 1:  # code for one cell machine
			if machine.col == col and machine.row == row:
				objectfound = machine
		elif machine.size == 2:  # code for one cell machine
			if machine.angle == 0 or machine.angle == 180 :
				if (machine.col == col and machine.row == row) or (machine.col  == col and machine.row + 1 == row):
					objectfound = machine
			else:
				if (machine.col == col and machine.row == row) or (machine.col + 1 == col and machine.row == row):
					objectfound = machine
	return objectfound


def get_colrow_from_coordinates(x, y):
	# works in W coordinates
	col = x // tile_size
	row = y // tile_size
	return col, row


def get_center_from_object(this):
	# works in W coordinates, for machine and Cargo
	x1_screen, y1_screen = this.rect.topleft
	x2_screen, y2_screen = this.rect.bottomright
	dx = x2_screen - x1_screen
	dy = y2_screen - y1_screen

	centerx, centery = this.x+dx, this.y+dy

	return centerx, centery


def get_tunnel_side(from_col, from_row, machine, side):
	# the method gives the side (Above or Below) of a tunnel, based on previous position vector .
	vectx = machine.col - from_col
	vecty = machine.row - from_row

	if vectx != 0:
		if machine.angle == 0 or machine.angle == 180:
			side = "Above"
		else:
			side = "Below"
	elif vecty != 0:
		if machine.angle == 0 or machine.angle == 180:
			side = "Below"
		else:
			side = "Above"
	print("tunnel side is ", side)
	return side


def get_connector_from_name(machine, connector_name):
	# only work for SIZE 1 and 2.
	# works in W coordinates
	connector_type = ""
	connector_state = False
	x, y, col, row ,vector_col, vector_row= 0, 0, 0, 0 , 0 ,0
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

	px = []
	py = []
	# col, row are delta col delta row
	adjcol = []
	adjrow = []

	if machine.size == 1:
		# 4 quadrants points (R,T,L,B) , before the rotation
		# ------------------------
		# size 1: one CELL
		#      T
		#   L[ X ] R
		#      B

		xr = tile_size
		yr = tile_size // 2
		colr = 1
		rowr = 0
		xt = tile_size // 2
		yt = 0
		colt = 0
		rowt = -1
		xl = 0
		yl = tile_size // 2
		coll = -1
		rowl = 0
		xb = tile_size // 2
		yb = tile_size
		colb = 0
		rowb = 1

		px.append(xr)
		py.append(yr)
		adjcol.append(colr)
		adjrow.append(rowr)

		px.append(xt)
		py.append(yt)
		adjcol.append(colt)
		adjrow.append(rowt)

		px.append(xl)
		py.append(yl)
		adjcol.append(coll)
		adjrow.append(rowl)

		px.append(xb)
		py.append(yb)
		adjcol.append(colb)
		adjrow.append(rowb)

		# if rotation
		if machine.angle == 0:
			j = 0
		if machine.angle == 90:
			j = 1
		if machine.angle == 180:
			j = 2
		if machine.angle == 270:
			j = 3

		# we affect correct values after rotation
		xr = px[j % 4]
		yr = py[j % 4]
		colr = adjcol[j % 4]
		rowr = adjrow[j % 4]

		xt = px[(j + 1) % 4]
		yt = py[(j + 1) % 4]
		colt = adjcol[(j + 1) % 4]
		rowt = adjrow[(j + 1) % 4]

		xl = px[(j + 2) % 4]
		yl = py[(j + 2) % 4]
		coll = adjcol[(j + 2) % 4]
		rowl = adjrow[(j + 2) % 4]

		xb = px[(j + 3) % 4]
		yb = py[(j + 3) % 4]
		colb = adjcol[(j + 3) % 4]
		rowb = adjrow[(j + 3) % 4]

		# ["Cnx_in_1" , "Face_L", "In" , True ]
		for connector in machine.T:
			if connector_name == connector[1]:
				connector_type = connector[2]
				connector_state = connector[3]

				if connector_name == "Face_R":
					x = xr
					y = yr
					col = colr
					row = rowr
				elif connector_name == "Face_T":
					x = xt
					y = yt
					col = colt
					row = rowt
				elif connector_name == "Face_L":
					x = xl
					y = yl
					col = coll
					row = rowl
				elif connector_name == "Face_B":
					x = xb
					y = yb
					col = colb
					row = rowb

	elif machine.size == 2:

		# 6 quadrants points (R1,T,L1,L2,B,R2) before the rotation
		# ------------------------
		# size 2: 2 CELLS vertical
		#      T
		# L1 [ X ] R1
		# L2 [ X ] R2
		#      B

		#possible point for 0 or 180
		#     1
		# 2 [ X ] 6
		# 3 [ X ] 5
		#     4

		#possible point for 90 or 270
		#     1    9
		# 2 [ X ][ X ] 8
		#     4    7

		x1 = tile_size // 2
		y1 = 0
		col1 = 0
		row1 = -1

		x2 = 0
		y2 = tile_size // 2
		col2 = -1
		row2 = 0

		x3 = 0
		y3 = 3*tile_size // 2
		col3 = -1
		row3 = 0

		x4 = tile_size // 2
		y4 = tile_size
		col4 = 0
		row4 = 1

		x5 = tile_size
		y5 = 3*tile_size // 2
		col5 = 1
		row5 = 0

		x6 = tile_size
		y6 = tile_size // 2
		col6 = 1
		row6 = 0

		x7 = 3*tile_size // 2
		y7 = tile_size
		col7 = 0
		row7 = 1

		x8 = 2*tile_size
		y8 = tile_size // 2
		col8 = 1
		row8 = 0

		x9 = 3*tile_size // 2
		y9 = 0
		col9 = 0
		row9 = -1

		for connector in machine.T:
			if connector_name == connector[1]:
				connector_type = connector[2]
				connector_state = connector[3]
				# if rotation
				if machine.angle == 0:
					if connector_name == "Face_R1":
						x = x6
						y = y6
						col = col6
						row = row6
					elif connector_name == "Face_T":
						x = x1
						y = y1
						col = col1
						row = row1
					elif connector_name == "Face_L1":
						x = x2
						y = y2
						col = col2
						row = row2
					elif connector_name == "Face_L2":
						x = x3
						y = y3
						col = col3
						row = row3
					elif connector_name == "Face_B":
						x = x4
						y = y4
						col = col4
						row = row4
					elif connector_name == "Face_R2":
						x = x5
						y = y5
						col = col5
						row = row5
				if machine.angle == 90:
					if connector_name == "Face_R1":
						x = x1
						y = y1
						col = col1
						row = row1
					elif connector_name == "Face_T":
						x = x2
						y = y2
						col = col2
						row = row2
					elif connector_name == "Face_L1":
						x = x4
						y = y4
						col = col4
						row = row4
					elif connector_name == "Face_L2":
						x = x7
						y = y7
						col = col7
						row = row7
					elif connector_name == "Face_B":
						x = x8
						y = y8
						col = col8
						row = row8
					elif connector_name == "Face_R2":
						x = x9
						y = y9
						col = col9
						row = row9
				if machine.angle == 180:
					if connector_name == "Face_R1":
						x = x3
						y = y3
						col = col3
						row = row3
					elif connector_name == "Face_T":
						x = x4
						y = y4
						col = col4
						row = row4
					elif connector_name == "Face_L1":
						x = x5
						y = y5
						col = col5
						row = row5
					elif connector_name == "Face_L2":
						x = x6
						y = y6
						col = col6
						row = row6
					elif connector_name == "Face_B":
						x = x1
						y = y1
						col = col1
						row = row1
					elif connector_name == "Face_R2":
						x = x2
						y = y2
						col = col2
						row = row2
				if machine.angle == 270:
					if connector_name == "Face_R1":
						x = x7
						y = y7
						col = col7
						row = row7
					elif connector_name == "Face_T":
						x = x8
						y = y8
						col = col8
						row = row8
					elif connector_name == "Face_L1":
						x = x9
						y = y9
						col = col9
						row = row9
					elif connector_name == "Face_L2":
						x = x1
						y = y1
						col = col1
						row = row1
					elif connector_name == "Face_B":
						x = x1
						y = y1
						col = col1
						row = row1
					elif connector_name == "Face_R2":
						x = x4
						y = y4
						col = col4
						row = row4

	# we set the coordinates in World Coordinates
	x = machine.x  + x
	y = machine.y  + y
	vector_col = col
	vector_row = row
	return connector_type, connector_state, x, y, vector_col, vector_row


def create_rel(machine, result):
	# create Relationship with other object , True if something was created
	result = False
	print("-----------------------------------------------------")
	print("Entering Relationship Creation for machine :", machine)

	# for every IN & OUT Port, we look for opposite port of others machines and create connection if COORD are matching

	for connector in machine.T:
		cnx_name = connector[1]
		cnx_type = ""
		cnx_state = ""
		# a relationship can be "Any", "Shape", or "Color"
		rel_type = "Any"
		cnx_x, cnx_y = 0, 0
		adjcol, adjrow = 0, 0
		cnx_type, cnx_state, cnx_x, cnx_y, adjcol, adjrow = get_connector_from_name(machine, cnx_name)

		# calculate the position of adjacent point, at the center of the cell
		xadj = cnx_x + tile_size//2*adjcol
		yadj = cnx_y + tile_size//2*adjrow

		print("Connector  :", cnx_name)
		print("calculate the position of adjacent point at   :", " x=" , xadj ,"/ ", "y=", yadj)

		# retrieve the machine at this point
		machine_adj = None
		machine_adj = find_machine_from_coord (xadj,yadj)

		# check if there is a port of opposite  type that matches the coord
		if machine_adj != None:
			cnx_name_adj, cnx_type_adj = machine_adj.get_connector_name_at_coord(cnx_x, cnx_y)

			if cnx_name_adj != "":

				# check opposition
				if (cnx_type == "In" and cnx_type_adj == "Out") or (cnx_type == "Out" and cnx_type_adj == "In"):

					print("we find one opposite port", cnx_name_adj, "of machine", machine_adj)
					result = True

					# calculating center of machines  in World Coordinates
					topleftx , toplefty = machine.rect.topleft
					x1t_screen, y1t_screen = topleftx, toplefty
					x1c_screen, y1c_screen = machine.rect.centerx ,machine.rect.centery
					dx =   x1c_screen - x1t_screen
					dy =   y1c_screen - y1t_screen
					x1 = machine.x + dx
					y1 = machine.y + dy

					topleftx, toplefty = machine_adj.rect.topleft
					x2t_screen, y2t_screen = topleftx, toplefty
					x2c_screen, y2c_screen = machine_adj.rect.centerx ,machine_adj.rect.centery
					dx = x2c_screen - x2t_screen
					dy = y2c_screen - y2t_screen
					x2 = machine_adj.x + dx
					y2 = machine_adj.y + dy
					# adding one relationship (always IN first to OUT)
					if cnx_type == "In":
						if isinstance(machine,c.Transformer):
							rel_type = "Shape"
							if isinstance(machine,c.Painter) and connector[1] == "Face_L2":
								rel_type = "Color"
						d.relationship_list.append([machine, connector[1], machine_adj, cnx_name_adj, rel_type, x1,y1,x2,y2])
					else:
						if isinstance(machine_adj,c.Transformer):
							rel_type = "Shape"
							if isinstance(machine_adj,c.Painter) and cnx_name_adj == "Face_L2":
								rel_type = "Color"
						d.relationship_list.append([machine_adj, cnx_name_adj, machine, connector[1], rel_type, x2,y2,x1,y1])

					# check relationship is created
					machine2 = None
					cnx_name2 = ""
					testresult = False
					machine2, cnx_name2, rel_type, testresult = get_rel(machine,connector[1])

	return result


def delete_rel(machine, result):
	i = 0
	# dump relationship before deleting
	print("dump relationship table before deleting")
	for relation in d.relationship_list:
		print(d.relationship_list[i][0], d.relationship_list[i][1], "//", d.relationship_list[i][2], d.relationship_list[i][3])
		i = i + 1

	# delete all Relationship involved with object , True if something was deleted
	for relation in d.relationship_list[:]:
		if machine == relation[0] or machine == relation[2]:
			# one relationship found
			print("we delete the relationship")
			print(relation[0], relation[1], "//", relation[2], relation[3])
			d.relationship_list.remove(relation)
			result = True

	return result


def get_rel(machine1, cnx_name1):
	# find Relationship with other object , Return  True if relationship exists,
	# return machine2 id and Connector Name 2, and the type of relationship
	result = False
	machine2 = None
	cnx_name2 = ""
	rel_type = ""

	for relation in d.relationship_list:
		if machine1 == relation[0] and cnx_name1 == relation[1]:
			# one relationship found
			machine2 = relation[2]
			cnx_name2 = relation[3]
			result = True

		if machine1 == relation[2] and cnx_name1 == relation[3]:
			# one relationship found
			machine2 = relation[0]
			cnx_name2 = relation[1]
			result = True

	return machine2, cnx_name2, rel_type, result


def draw_rel(screen, camera):
	# draw all connection lines
	# works in S coordinates (camera needed)
	for relation in d.relationship_list:
		pygame.draw.line(screen, RED, (relation [5] - camera.offsetx, relation [6]-camera.offsety), (relation [7]- camera.offsetx, relation [8]- camera.offsety))


def shape_vertical_cut(code_dna_in):
	# we split the cargo vertically. the DNA code In, is getting split into two codes
	# the method encode dna om a custom shape, from a formatted string "code"
	# for instance "S1d/s/s/s/s:C2g/n/r/s/s:N0d/n/n/n/n:C1y/s/s/n/n"
	print("---------------------------------------------------")
	print("Entering v cut with  dna = ", code_dna_in)

	# how many layers
	layers = code_dna_in.split("&")
	layer_count = 0
	string_separator = ""
	code_dna_out_right = ""
	code_dna_out_left  = ""

	for layer in layers:
		# get each quadrant of a given layer and rotate
		q= layer.split(":")
		if q[0][0:1] != "N" or q[3][0:1] !="N":
			code_tmp_right= q[0]          + ":" + "N0d/n/n/n/n:N0d/n/n/n/n" + ":" + q[3]
		else:
			code_tmp_right =""
		if q[1][0:1] != "N" or q[2][0:1] != "N":
			code_tmp_left = "N0d/n/n/n/n" + ":" + q[1]  + ":" + q[2] + ":" + "N0d/n/n/n/n"
		else:
			code_tmp_left =""

		# we avoid empty layer
		if layer_count !=0:
			string_separator ="&"
		if code_tmp_right!="":
			code_dna_out_right = code_dna_out_right + string_separator + code_tmp_right
		if code_tmp_left!="":
			code_dna_out_left  = code_dna_out_left  + string_separator + code_tmp_left

		layer_count +=1



	print("code right = ", code_dna_out_right)
	print("code left  = ", code_dna_out_left)
	print("---------------------------------------------------")

	return code_dna_out_left, code_dna_out_right


def shape_rotate(code_dna_in, angle):
	# we rotate the  DNA
	# the method encode dna om a custom shape
	# for instance S/s/s/s/s:R/n/r/s/s:N/n/n/n/n:C/s/s/n/n
	print("---------------------------------------------------")
	print("Entering rotator with top dna = ", code_dna_in, " and angle = ", angle)

	# how many layers
	layers = code_dna_in.split("&")
	layer_count = 0
	string_separator = ""
	code_dna_out = ""

	for layer in layers:
		# get each quadrant of a given layer and rotate
		q= layer.split(":")

		if angle == 90:
			code_tmp = q[3]+":"+q[0]+":"+q[1]+":"+q[2]
		elif angle == 180:
			code_tmp = q[2]+":"+q[3]+":"+q[0]+":"+q[1]
		elif angle == 270:
			code_tmp = q[1]+":"+q[2]+":"+q[3]+":"+q[0]

		if layer_count !=0:
			string_separator ="&"
		code_dna_out = code_dna_out + string_separator + code_tmp
		layer_count +=1

	print("code after rotation = ", code_dna_out)
	print("---------------------------------------------------")

	return code_dna_out


def shape_assemble(code_dna_bot , code_dna_top):
	# we assemble two DNA
	# we superimpose top on bottom.
	# rules for assembler.
	#   no stacking above 4, above it is simply ignored
	#   fibo scaling happens if at least one quadrant overlaps
	#   if no overalp, shapes are reset to 1 when they "fall" on layer 0
	#

	print("---------------------------------------------------")
	print ("Entering assembler with top dna = ", code_dna_top , " and code bottom = ", code_dna_bot )

	bot_q = []
	tmp_q = code_dna_bot.split("&")
	for layer in tmp_q:
		tmp = layer.split(":")
		bot_q.append(tmp)

	top_q = []
	tmp_q = code_dna_top.split("&")
	for layer in tmp_q:
		tmp = layer.split(":")
		top_q.append(tmp)

	q_res = []

	# method to determine if quadrant overlaps, to trigger the scaling or not
	overlap = False
	j = 0

	while j < 4:
		print("we compare quadrant", j)
		print("bot_q ", bot_q[0][j][0:3])
		print("top_q ", top_q[0][j][0:3])
		if bot_q[0][j][0:3] != "N0d" and top_q[0][j][0:3] != "N0d":
			overlap = True
		j = j + 1
	print("is the merge  overalaping? ", overlap)

	tmp_stack = []

	q0_fin_stack = []
	q1_fin_stack = []
	q2_fin_stack = []
	q3_fin_stack = []

	print("-------------------------------------------------------------")
	k = 0
	while k < 4:
		print("quadrant #", k)
		for layer in bot_q:
			# we fill the stacks
			tmp_stack.append(layer[k])

		layer_max_bot = len(tmp_stack)
		print("number of layer in this quadrant", layer_max_bot)

		for layer in top_q:
			# we fill the stacks
			tmp_stack.append(layer[k])

		# we analyze each the quadrant k , and we traverse the layer
		i = 0
		delta_overlap = 0
		level_previous = 0
		for quadrant in tmp_stack:
			if quadrant[0:3] == "N0d" and overlap and i < layer_max_bot:
				# we initialize to 1 the level only there is not another higher value
				if level_previous == 0:
					level_previous = 1
				i = i + 1
			if quadrant[0:3] != "N0d":
				if i < layer_max_bot:
					if k == 0:
						q0_fin_stack.append(quadrant)
					elif k == 1:
						q1_fin_stack.append(quadrant)
					elif k == 2:
						q2_fin_stack.append(quadrant)
					elif k == 3:
						q3_fin_stack.append(quadrant)

					level_previous = int(quadrant[1:2])
					print("add bot quadrant", quadrant, "level #", level_previous)
				else:
					# staking begins
					level_current = int(quadrant[1:2])
					level_current = max(level_current, level_previous)
					level_current = level_current + 1
					quadrant = quadrant[0:1] + str(level_current) + quadrant[2:]
					# we don’t authorize level superior to 4
					if level_current > 4:
						break
					if k == 0:
						q0_fin_stack.append(quadrant)
					elif k == 1:
						q1_fin_stack.append(quadrant)
					elif k == 2:
						q2_fin_stack.append(quadrant)
					elif k == 3:
						q3_fin_stack.append(quadrant)

					level_previous = level_current
				i = i + 1
		k = k + 1
		tmp_stack.clear()

	print("---------------------results ----------------------------------------")
	mlax0 = len(q0_fin_stack)
	for quadrant in q0_fin_stack:
		print("quadrant final 0", quadrant)
	print("max length ", mlax0)
	mlax1 = len(q1_fin_stack)
	for quadrant in q1_fin_stack:
		print("quadrant final 1", quadrant)
	print("max length ", mlax1)
	mlax2 = len(q2_fin_stack)
	for quadrant in q2_fin_stack:
		print("quadrant final 2", quadrant)
	print("max length ", mlax2)
	mlax3 = len(q3_fin_stack)
	for quadrant in q3_fin_stack:
		print("quadrant final 3", quadrant)
	print("max length ", mlax3)

	print("---------------------writing q_res ----------------------------------------")
	# rebuilding a final block
	maxtotal = max(mlax0, mlax1, mlax2, mlax3)
	i = 0
	while i < maxtotal:
		if i > mlax0 - 1:
			q0tmp = 'N0d/n/n/n/n'
		else:
			q0tmp = q0_fin_stack[i]
		if i > mlax1 - 1:
			q1tmp = 'N0d/n/n/n/n'
		else:
			q1tmp = q1_fin_stack[i]
		if i > mlax2 - 1:
			q2tmp = 'N0d/n/n/n/n'
		else:
			q2tmp = q2_fin_stack[i]
		if i > mlax3 - 1:
			q3tmp = 'N0d/n/n/n/n'
		else:
			q3tmp = q3_fin_stack[i]
		q_res.append([q0tmp, q1tmp, q2tmp, q3tmp])
		i = i + 1

	# rebuilding the string
	layer_count = 0
	code_out = ""
	layer_separator = "&"

	for layer in q_res:
		quadrant_count = 0
		quadrant_separator = ""

		for quadrant in layer:
			if quadrant_count != 0:
				quadrant_separator = ":"
			code_out = code_out + quadrant_separator + quadrant
			quadrant_count += 1

		if layer_count < maxtotal - 1:
			layer_separator = "&"
		else:
			layer_separator = ""
		code_out = code_out + layer_separator
		layer_count += 1


	print("code after assembling = ", code_out)
	print("---------------------------------------------------")

	return code_out


def get_color_from_string(quadrant):
	# provide a color from a string quadrant.
	# S1d/s/s/s/s
	color = GREY
	string = quadrant [2:3]
	if string == "d":
		color = GREY
	elif string == "r":
		color = RED
	elif string == "g":
		color = GREEN
	elif string == "b":
		color = BLUE
	elif string == "y":
		color = YELLOW
	elif string == "c":
		color = CYAN
	elif string == "m":
		color = MAGENTA
	elif string == "w":
		color = WHITE

	return color


def shape_color(code_dna_in, color):
	# the method encode color on DNA for all Quadrant of a custom shape
	# for instance "S1d/s/s/s/s:C2g/n/r/s/s:N0d/n/n/n/n:C1y/s/s/n/n" and color WHITE w
	# becomes      "S1w/s/s/s/s:C2w/n/r/s/s:N0d/n/n/n/n:C1w/s/s/n/n"
	# empty quadrant dont have color

	print (" code before  color change", code_dna_in)
	code_dna_out = ""

	if color == GREY:
		string = "d"
	elif color == RED:
		string = "r"
	elif color == GREEN:
		string = "g"
	elif color == BLUE:
		string = "b"
	elif color == YELLOW:
		string = "y"
	elif color == CYAN:
		string = "c"
	elif color == MAGENTA:
		string = "m"
	elif color == WHITE:
		string = "w"

	# how many layers
	layers = code_dna_in.split("&")
	layer_count = 0
	string_separator = ""

	for layer in layers:
		# get each quadrant
		q= layer.split(":")

		q0 = q[0][0:2] + string + q[0][3:]
		q1 = q[1][0:2] + string + q[1][3:]
		q2 = q[2][0:2] + string + q[2][3:]
		q3 = q[3][0:2] + string + q[3][3:]

		if layer_count !=0:
			string_separator ="&"
		code_dna_out = code_dna_out + string_separator + q0 + ":" + q1 + ":" + q2 + ":" + q3
		layer_count +=1


	print ("new code after color change", code_dna_out)

	return code_dna_out


def generate_random_dna (size,layer,difficulty):
	# provide a dna from
	# size (1,2,3,4) , corresponding to 1 cell, 2 cells, 3 cells or 4 cells
	# layer (1,2,3,4)
	# difficulty : easy, medium, hard
	'''dna_code_out = "S2b/n/n/n/n:C2r/n/n/n/n:C1y/n/n/n/n:T1r/n/n/n/n"'''

	quadrant_type_list = ["S", "C", "T"]
	quadrant_color_list = ["r", "g", "b", "y", "c", "m", "w", "d"]
	# "S2b/n/n/n/n:C2r/n/n/n/n:C2b/n/n/n/n:T2r/n/n/n/n"
	# "S1d/n/n/n/n:S1d/n/n/n/n:S1d/n/n/n/n:S1d/n/n/n/n"

	# temporary : we force the size to 1
	size = 1
	layer = 4
	first_quadrant = True

	'''random.seed(26)'''

	# how many layers?
	layer_count = random.randint(1, layer)
	layer_count = 4
	print("number of layers", layer_count)
	i = 1

	code_dna_list = []

	# this list tracks the open quadrant to avoid populating a quadrant
	# if the quadrant below is NONE
	# if the quadrant below if at level 4 (max)
	overall_quadrant_available = [1, 2, 3, 4]
	quadrant_tmp = []

	# this list tracks the availability of quadrant overall
	main_quadrant_slot_list = [1, 2, 3, 4]

	while i <= layer_count:
		# how many quadrant in this layer?
		# the first layer must have at least 2 quadrants
		# the first quadrant must be of size 1 (Anchor)
		# we limit the number of quadrant to the max
		if i == 1:
			quadrant_count = random.randint(2, len(main_quadrant_slot_list))
		else:
			quadrant_count = random.randint(1, len(main_quadrant_slot_list))
		print("number of quadrants", quadrant_count)
		j = 1

		quadrant_slot_list = main_quadrant_slot_list.copy()

		while j <= quadrant_count:

			# which slot
			quadrant_slot_select = random.choice(quadrant_slot_list)

			# which type
			quadrant_type = random.choice(quadrant_type_list)

			# which color
			quadrant_color = random.choice(quadrant_color_list)

			# which size, we must restrain the size to be higher than the sub-quadrant
			'''quadrant_size = random.randint(1, 4)'''
			if i == 1:
				min_size = 1
				max_size = 2
				if first_quadrant:
					max_size = 1
					first_quadrant = False
			else:
				index = (i - 2) * 4 + quadrant_slot_select - 1
				min_size = quadrant_tmp[index][3] + 1
				max_size = 4

			if min_size > 4:
				quadrant_size = 0
				quadrant_type = "N"
				quadrant_color = "d"
			else:
				quadrant_size = random.randint(min_size, max_size)

			print("layer ", i, "Slot =", quadrant_slot_select, "Shape Type", quadrant_type, " Size =", quadrant_size,
			      "Color ", quadrant_color)

			# we fill a temporatry list for the layer
			quadrant_tmp.append([i, quadrant_slot_select, quadrant_type, quadrant_size, quadrant_color])

			# remove the slot from the potential list of quadrant
			quadrant_slot_list.remove(quadrant_slot_select)
			j += 1

		# we write the layer code in correct order

		# clean up, we must ensure we have 4 quadrants for layer i
		k = 1
		q0found = False
		q1found = False
		q2found = False
		q3found = False

		for quadrant in quadrant_tmp:
			# we filter on the layer
			if i == quadrant[0]:
				# we check the quadrant
				if quadrant[1] == 1:
					q0found = True
				elif quadrant[1] == 2:
					q1found = True
				elif quadrant[1] == 3:
					q2found = True
				elif quadrant[1] == 4:
					q3found = True

		# at the end of the scan, if not found we must add an empty quadrant
		if not q0found:
			quadrant_tmp.append([i, 1, "N", 0, "d"])
			if 1 in main_quadrant_slot_list: main_quadrant_slot_list.remove(1)
		if not q1found:
			quadrant_tmp.append([i, 2, "N", 0, "d"])
			if 2 in main_quadrant_slot_list: main_quadrant_slot_list.remove(2)
		if not q2found:
			quadrant_tmp.append([i, 3, "N", 0, "d"])
			if 3 in main_quadrant_slot_list: main_quadrant_slot_list.remove(3)
		if not q3found:
			quadrant_tmp.append([i, 4, "N", 0, "d"])
			if 4 in main_quadrant_slot_list: main_quadrant_slot_list.remove(4)

		quadrant_tmp = sorted(quadrant_tmp)

		# if this entire layer was added but empty, the generation stops.
		index = (i - 1) * 4
		if quadrant_tmp[index][2] == "N" and quadrant_tmp[index + 1][2] == "N" and quadrant_tmp[index + 2][2] == "N" and \
				quadrant_tmp[index + 3][2] == "N":
			print("we popped the last layer")
			quadrant_tmp.pop()
			quadrant_tmp.pop()
			quadrant_tmp.pop()
			quadrant_tmp.pop()
			break

		i += 1

	quadrant_tmp = sorted(quadrant_tmp)

	for quadrant in quadrant_tmp:
		print("--", quadrant)

	# rebuilding the string
	layer_count = 0
	dna_code_out = ""
	layer_separator = "&"
	i = 0
	quadrant_count = 0

	for quadrant in quadrant_tmp:

		quadrant_separator = ""

		code_tmp = quadrant[2] + str(quadrant[3]) + quadrant[4] + "/n/n/n/n"
		if quadrant_count != 0  and quadrant_count % 4 !=0:
			quadrant_separator = ":"

		dna_code_out = dna_code_out + quadrant_separator + code_tmp
		quadrant_count += 1

		if quadrant_count % 4 == 0 and quadrant_count != len(quadrant_tmp):
			layer_separator = "&"
			dna_code_out = dna_code_out + layer_separator

		layer_count += 1
		print("Final code out", dna_code_out)

	'''dna_code_out = "C1g/n/n/n/n:S1d/n/n/n/n:C1g/n/n/n/n:S1r/n/n/n/n&S2b/n/n/n/n:C2r/n/n/n/n:C2b/n/n/n/n:T2r/n/n/n/n"'''

	return dna_code_out









