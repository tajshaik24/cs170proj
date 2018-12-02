import random
import os
import networkx as nx
shuffle = random.shuffle

def main():
	G = readInput("all_inputs/small/119/")
	encode = {}
	decode = {}
	labelID = 0
	for node in G.nodes:
		encode[node] = labelID
		decode[labelID] = node
		labelID += 1

	s = [i for i in range(50)]
	shuffle(s)
	bus_arrangements = [[] for i in range(16)]
	for i in range(len(bus_arrangements)):
		x = s.pop()
		bus_arrangements[i].append(x)
	while s:
		busNum = random.randint(0, 15)
		bus_arrangements[busNum].append(s.pop())

	for i in range(len(bus_arrangements)):
		for j in range(len(bus_arrangements[i])):
			bus_arrangements[i][j] = decode[bus_arrangements[i][j]]

	folder = "all_outputs/small/119/"
	writeOutput(bus_arrangements, folder)




def readInput(inputFolder):
	graph = nx.read_gml(inputFolder + "graph.gml")
	return graph




def writeOutput(bus_arrangements, folder):
	print(bus_arrangements)
	if not os.path.exists(folder):
		os.makedirs(folder)
	file = folder + '.out'
	with open(file, 'w') as f:
		for bus in bus_arrangements:
			f.write("%s\n" % bus)
	f.close()


if __name__ == '__main__':
	main()