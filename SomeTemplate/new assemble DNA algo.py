
qz= 50

code_dna_bot = "N0d/n/n/n/n:T2s/n/n/n/n:S1d/n/n/n/n:N0d/n/n/n/n"
code_dna_top = "S1w/n/n/n/n:N0d/n/n/n/n:N0d/n/n/n/n:S1b/n/n/n/n"

bot_q =[]
tmp_q = code_dna_bot.split("&")
for layer in tmp_q:
	tmp = layer.split(":")
	bot_q.append(tmp)

top_q =[]
tmp_q = code_dna_top.split("&")
for layer in tmp_q:
	tmp = layer.split(":")
	top_q.append(tmp)

q_res = []

# method to determine if quadrant overlaps, to trigger the scaling or not
overlap = False
j=0

while j < 4:
	print ("we compare quadrant",j)
	print("bot_q ", bot_q [0][j][0:3])
	print("top_q ", top_q [0][j][0:3])
	if bot_q [0][j][0:3] !="N0d" and top_q [0][j][0:3] !="N0d":
		overlap = True
	j=j+1
print ("is the merge  overalaping? ",overlap)

tmp_stack  =[]

q0_fin_stack  =[]
q1_fin_stack  =[]
q2_fin_stack  =[]
q3_fin_stack  =[]

print("-------------------------------------------------------------")
k = 0
while k < 4:
	print ("quadrant #", k)
	for layer in bot_q:
		# we fill the stacks
	    tmp_stack.append (layer[k])

	layer_max_bot = len(tmp_stack)
	print ("number of layer in this quadrant",layer_max_bot)

	for layer in top_q:
		# we fill the stacks
		tmp_stack.append (layer[k])

	# we analyze each the quadrant k , and we traverse the layer
	i=0
	delta_overlap = 0
	level_previous = 0
	for quadrant in tmp_stack:
		if quadrant[0:3] == "N0d" and overlap and i < layer_max_bot:
			# we initialize to 1 the level only there is not another higher value
			if level_previous ==0:
				level_previous = 1
			i = i+1
		if quadrant[0:3] != "N0d":
			if i < layer_max_bot:
				if k==0:
					q0_fin_stack.append(quadrant)
				elif k==1:
					q1_fin_stack.append(quadrant)
				elif k==2:
					q2_fin_stack.append(quadrant)
				elif k==3:
					q3_fin_stack.append(quadrant)

				level_previous = int(quadrant [1:2])
				print ("add bot quadrant", quadrant, "level #" ,level_previous)
			else:
				# staking begins
				level_current = int(quadrant[1:2])
				level_current = max (level_current,level_previous)
				level_current = level_current + 1
				quadrant = quadrant[0:1]+str(level_current)+quadrant[2:]
				# we don’t authorize level superior to 4
				if level_current > 4:
					break
				if k==0:
					q0_fin_stack.append(quadrant)
				elif k==1:
					q1_fin_stack.append(quadrant)
				elif k==2:
					q2_fin_stack.append(quadrant)
				elif k==3:
					q3_fin_stack.append(quadrant)

				level_previous = level_current
			i = i + 1
	k=k+1
	tmp_stack.clear()


print("---------------------results ----------------------------------------")
mlax0= len(q0_fin_stack)
for quadrant in q0_fin_stack:
	print ("quadrant final 0",quadrant)
print("max length ", mlax0)
mlax1= len(q1_fin_stack)
for quadrant in q1_fin_stack:
	print ("quadrant final 1",quadrant)
print ("max length ",mlax1)
mlax2=len(q2_fin_stack)
for quadrant in q2_fin_stack:
	print ("quadrant final 2",quadrant)
print("max length ",mlax2)
mlax3= len(q3_fin_stack)
for quadrant in q3_fin_stack:
	print ("quadrant final 3",quadrant)
print("max length ",mlax3)


print("---------------------writing q_res ----------------------------------------")
# rebuilding a final block
maxtotal = max (mlax0,mlax1,mlax2,mlax3)
i=0
while i < maxtotal :
	if i>mlax0-1:
		q0tmp ='N0d/n/n/n/n'
	else:
		q0tmp= q0_fin_stack[i]
	if i>mlax1-1:
		q1tmp ='N0d/n/n/n/n'
	else:
		q1tmp= q1_fin_stack[i]
	if i>mlax2-1:
		q2tmp ='N0d/n/n/n/n'
	else:
		q2tmp= q2_fin_stack[i]
	if i>mlax3-1:
		q3tmp ='N0d/n/n/n/n'
	else:
		q3tmp= q3_fin_stack[i]
	q_res.append([q0tmp,q1tmp,q2tmp,q3tmp])
	i=i+1

# rebuilding the string
layer_count = 0
code_tmp = ""
layer_separator = "&"

for layer in q_res:
	quadrant_count = 0
	quadrant_separator = ""

	for quadrant in layer:
		if quadrant_count != 0:
			quadrant_separator = ":"
		code_tmp = code_tmp + quadrant_separator + quadrant
		quadrant_count += 1

	if layer_count < maxtotal-1:
		layer_separator = "&"
	else:
		layer_separator = ""
	code_tmp = code_tmp + layer_separator
	layer_count += 1

print ("final dna", code_tmp )
