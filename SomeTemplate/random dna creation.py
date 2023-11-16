import random
# provide a dna from
# size (1,2,3,4) , corresponding to 1 cell, 2 cells, 3 cells or 4 cells
# layer (1,2,3,4)
# difficulty : easy, medium, hard
dna_code_out = "S2b/n/n/n/n:C2r/n/n/n/n:C1y/n/n/n/n:T1r/n/n/n/n"
# fibonaci quadrant size :5->3->2->1
'''quadrant_type_list = {'0': "N", '1': "S", '2': "C" , '3' : "T"}'''

quadrant_type_list = ["S", "C", "T"]
quadrant_color_list = ["r","g","b","y","c","m","w","d"]
# "S2b/n/n/n/n:C2r/n/n/n/n:C2b/n/n/n/n:T2r/n/n/n/n"
# "S1d/n/n/n/n:S1d/n/n/n/n:S1d/n/n/n/n:S1d/n/n/n/n"

# temporary : we force the size to 1
size = 1
layer = 4

random.seed(26)

# how many layers?
layer_count = random.randint (1,layer)
layer_count = 4
print ("number of layers", layer_count)
i   = 1

code_dna_list =[]

# this list tracks the open quadrant to avoid populating a quadrant
# if the quadrant below is NONE
# if the quadrant below if at level 4 (max)
overall_quadrant_available = [1, 2, 3, 4]
quadrant_tmp = []

#this list tracks the availability of quadrant overall
main_quadrant_slot_list = [1, 2, 3, 4]

while i <=layer_count:
	# how many quadrant in this layer?
	# the first layer must have at least 2 quadrants
	# we limit the number of quadrant to the max
	if i==1:
		quadrant_count  = random.randint(2, len(main_quadrant_slot_list ))
	else:
		quadrant_count = random.randint(1, len(main_quadrant_slot_list ))
	print("number of quadrants", quadrant_count)
	j = 1

	quadrant_slot_list = main_quadrant_slot_list.copy()


	while j <= quadrant_count:

		# which slot
		quadrant_slot_select = random.choice (quadrant_slot_list)

		# which type
		quadrant_type = random.choice (quadrant_type_list)

		# which color
		quadrant_color = random.choice (quadrant_color_list)

		# which size, we must restrain the size to be higher than the sub-quadrant
		'''quadrant_size = random.randint(1, 4)'''
		if i ==1 :
			min_size =1
		else:
			index = (i-2)*4+quadrant_slot_select-1
			min_size = quadrant_tmp [index][3]+1

		if min_size>4:
			quadrant_size = 0
			quadrant_type = "N"
			quadrant_color = "d"
		else:
			quadrant_size = random.randint(min_size,4)


		print ("layer ", i,"Slot =",quadrant_slot_select, "Shape Type" ,quadrant_type, " Size =" ,quadrant_size, "Color ",quadrant_color)

		# we fill a temporatry list for the layer
		quadrant_tmp.append( [i, quadrant_slot_select, quadrant_type ,quadrant_size,quadrant_color] )

		#remove the slot from the potential list of quadrant
		quadrant_slot_list.remove(quadrant_slot_select)
		j+=1

		# we write the layer code in correct order

	# clean up, we must ensure we have 4 quadrants for layer i
	k=1
	q0found = False
	q1found = False
	q2found = False
	q3found = False

	for quadrant in quadrant_tmp:
			# we filter on the layer
			if i == quadrant[0]:
				#we check the quadrant
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
		quadrant_tmp.append([i, 1, "N", 0,"d"])
		if 1 in main_quadrant_slot_list:main_quadrant_slot_list.remove(1)
	if not q1found:
		quadrant_tmp.append([i, 2, "N", 0,"d"])
		if 2 in main_quadrant_slot_list:main_quadrant_slot_list.remove(2)
	if not q2found:
		quadrant_tmp.append([i, 3, "N", 0,"d"])
		if 3 in main_quadrant_slot_list:main_quadrant_slot_list.remove(3)
	if not q3found:
		quadrant_tmp.append([i, 4, "N", 0,"d"])
		if 4 in main_quadrant_slot_list:main_quadrant_slot_list.remove(4)

	quadrant_tmp = sorted(quadrant_tmp)

	# if this entire layer was added but empty, the generation stops.
	index = (i - 1) * 4
	if quadrant_tmp [index][2] == "N" and  quadrant_tmp [index+1][2] == "N" and quadrant_tmp [index+2][2] == "N" and quadrant_tmp [index+3][2] == "N":
		print ("we popped the last layer")
		quadrant_tmp.pop()
		quadrant_tmp.pop()
		quadrant_tmp.pop()
		quadrant_tmp.pop()
		break

	i+=1

quadrant_tmp = sorted(quadrant_tmp)

for quadrant in quadrant_tmp:
	print("--", quadrant)


# rebuilding the string
layer_count = 0
code_out = ""
layer_separator = "&"
i=0
quadrant_count = 0


for quadrant in quadrant_tmp:

	quadrant_separator = ""

	code_tmp = quadrant [2]+ str(quadrant [3]) + quadrant [4] + "/n/n/n/n"
	if quadrant_count != 0 and quadrant_count % 4 !=0:
		quadrant_separator = ":"

	code_out = code_out + quadrant_separator + code_tmp
	quadrant_count += 1

	if quadrant_count % 4 ==0 and quadrant_count != len(quadrant_tmp):
		layer_separator = "&"
		code_out = code_out + layer_separator

	layer_count += 1
	print("Final code out", code_out)
