
class Part:
	def __init__(self, name):
		self.name = name

part1 = Part ("part1")
part2 = Part ("part2")
part3 = Part ("part3")
part4 = Part ("part4")
part5 = Part ("part5")
part6 = Part ("part6")
part7 = Part ("part7")

relationship_list= []



relationship_list= [
    [part1, "Face_R", part2, "Face_L",  False],
    [part3, "Face_B", part4, "Face_T",  False],
    [part5, "Face_R", part2, "Face_L",  False],
    [part6, "Face_B", part7, "Face_T",  False],
    [part1, "Face_L", part3, "Face_T" , False]
                    ]

numrows = len(relationship_list)
print (numrows )
i=0
while i < numrows:
    print (relationship_list [i][0].name,relationship_list [i][1],"//",relationship_list [i][2].name,relationship_list [i][3] )
    i = i+1


#loop overfirst column, delete all occurences

for relation in relationship_list [:]:
    if relation [0] == part3  or relation [2] == part3:
        print ("part1/find Face_R")
        relationship_list.remove(relation)



numrows = len(relationship_list)
print (numrows )
i=0
while i < numrows:
    print (relationship_list [i][0].name,relationship_list [i][1],"//",relationship_list [i][2].name,relationship_list [i][3] )
    i = i+1

