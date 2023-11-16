

class Part:
	def __init__(self, name):
		self.name = name

part1 = Part ("Conveyor")
part2 = Part ("Conveyor")
part3 = Part ("Conveyor")
part4 = Part ("Splitter")

relationship_list = {"Part In":[], "Connector In":[],"Part Out":[],"Connector Out":[] ,"Type":[] }


relationship_list["Part In"] .append(part1)
relationship_list["Part Out"].append(part2)
relationship_list["Connector In"] .append("Face_R")
relationship_list["Connector Out"] .append("Face_L")
relationship_list["Type"] .append("Cargo")

relationship_list["Part In"] .append(part3)
relationship_list["Part Out"].append(part4)
relationship_list["Connector In"] .append("Face_B")
relationship_list["Connector Out"] .append("Face_T")
relationship_list["Type"] .append("Cargo")

print(relationship_list)

keys = relationship_list.items()
print(keys)


