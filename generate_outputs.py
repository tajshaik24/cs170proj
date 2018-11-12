import networkx as nx
import os
import matplotlib.pyplot as plt
import random

def main():
    generateOutputs('small')
    generateOutputs('medium')
    generateOutputs('large')

def generateOutputs(folder):
    if not os.path.exists(folder):
        return
    if folder == 'small':
        num_of_friends = 50
    if folder == 'medium':
        num_of_friends = 500
    if folder == 'large':
        num_of_friends = 1000
    file = folder + '/parameters.txt'
    with open(file, 'r') as f:
        numOfTables = f.readline()
        sizePerTable = f.readline()
    f.close()
    bus_arrangements = []
    nodes_used = [i for i in range(1, num_of_friends+1)]
    randSize = int(num_of_friends/int(numOfTables))
    for i in range(int(numOfTables)):
        bus = []
        if i == int(numOfTables)-1:
            for i in range(num_of_friends):
                student = random.choice(nodes_used)
                nodes_used.remove(student)
                bus.append(student)
        else:
            num_of_friends = num_of_friends - randSize
            for i in range(randSize):
                student = random.choice(nodes_used)
                nodes_used.remove(student)
                bus.append(student)
        bus_arrangements.append(bus)
    file = folder + '.out'
    with open(file, 'w') as f:
        for bus in bus_arrangements:
            f.write("%s\n" % bus)
    f.close()

if __name__ == '__main__':
    main()