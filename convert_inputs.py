import networkx as nx
import os
import matplotlib.pyplot as plt
import random

def main():
    friendships, string = writeFriendships('large')
    writeToFile('small', friendships, string)


def writeFriendships(folder):
    all_friendships = set()
    string = []
    if not os.path.exists(folder):
        return {},[]
    path = folder + '/graph.gml'
    graph = nx.read_gml(path)
    e = graph.edges()
    for edge in e:
        all_friendships.add(edge)
        string.append(str(edge[0]) + " " + str(edge[1]) + " " + "F")
    return all_friendships, string

# TODO: Must finish this
def writeEnemies(folder, friends, list_friends):
    if not os.path.exists(folder):
            return
    if folder == 'small':
        num_of_friends = 50
    if folder == 'medium':
        num_of_friends = 500
    if folder == 'large':
        num_of_friends = 1000
    file = folder + '/parameters.txt'
    enemy_list = []
	with open(file, 'r') as f:
		numOfTables = f.readline()
		sizePerTable = f.readline()
		for x in f:
			enemy_list.append(x)
	f.close()
    file = folder + '.txt'
	with open(file, 'w') as f:
		f.write(str(num_of_friends))
		f.write(str(numOfTables) + '\n')
		for x in rowdyGroups:
			f.write("%s\n" % x)
	f.close()

if __name__ == '__main__':
    main()