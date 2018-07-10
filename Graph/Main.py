import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from string import ascii_lowercase

def drwinput():
    foo = open('testcase.txt', 'r')

    j = []
    for i in foo.readlines():
        if '\n' in i:
            i = i[0:-1]
        j.append(i.split(' '))

    size = int(j[0][0])
    j.remove(j[0])

    for i in j:
        for s in range(len(i) - 1):
            if int(i[s]) > size:
                i[s] = int(i[s]) - size
    for i in j:
        for s in range(len(i)):
            if type(i[s]) == str:
                i[s] = int(i[s])



    final = [[0 for i in range(size)] for s in range(size)]
    tmp = []

    for i in range(0, len(j)):
        tmp.append(j[i][2])

    String = ''
    for i in tmp:
        String += str(i)


    tmp2 = []
    for i in range(0, len(tmp), size):
        tmp2.append(tmp[i:i + size])

    s = open('inputvisual.txt', 'w')
    s.write(str(size) + '\n')
    for i in tmp2:
        String1 = ''
        for f in i:
            String1 += str(f) + ' '
        s.write(String1 + '\n')


drwinput()

a = open('testcase.txt', 'r')


foo = a.readlines()
counter = 0

initial_list = []
matrix = []
for line in foo:
    if counter == 0:
        initial_list = line.split()
    if counter == 1:
        matrix.append(line.split())
    counter = 1

graph = {}
for i in range(len(matrix)):
    for j in range(int(initial_list[0])):
        if j % int(initial_list[0]) == 0:
            if int(matrix[i][0]) not in graph:
                graph[int(matrix[i][0])] = set()
        if j % int(initial_list[0]) != 0:
            if int(matrix[i][1]) not in graph:
                graph[int(matrix[i][1])] = set()

for i in graph:
    for j in range(len(matrix)):
        if str(i) in matrix[j][:2]:
            if i != int(matrix[j][1]):
                graph[i].add(int(matrix[j][1]))
                graph[int(matrix[j][1])].add(i)

edge_cost = {}
for i in range(len(matrix)):
    edge_cost[(int(matrix[i][0]), int(matrix[i][1]))] = int(matrix[i][2])
    edge_cost[(int(matrix[i][1]), int(matrix[i][0]))] = int(matrix[i][2])

state = {}

for i in graph:
    state[i] = 'unmatched'

vertex_cost = {}
for i in graph:
    vertex_cost[i] = 0

L = []
R = []
for i in graph:
    if i < int(initial_list[0]) + 1:
        L.append(i)
    else:
        R.append(i)


def bfs_paths(graph, start):
    global edge_cost
    global vertex_cost

    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if edge_cost[(vertex, next)] - vertex_cost[vertex] - vertex_cost[next] == 0:
                if state[next] == 'matched':
                    queue.append((next, path + [next]))

                else:
                    return path + [next]

    return path
    # else:
    #     queue.append((next, path + [next]))


matching = []

counter = 0
while True:
    if counter >= len(L):
        break
    unmatched_vertex = L[counter]
    state[unmatched_vertex] = 'matched'

    good_path = bfs_paths(graph, unmatched_vertex)
    has_unmatched_vertex = False
    for i in good_path:
        if state[i] == 'unmatched':
            has_unmatched_vertex = True
        else:
            has_unmatched_vertex = False

    if has_unmatched_vertex:
        # print(good_path)
        matching.append(good_path)
        for i in good_path:
            state[i] = 'matched'
        counter += 1

    if not has_unmatched_vertex:
        S = []
        Ns = []

        for i in range(len(good_path)):
            if i % 2 == 0:
                S.append(good_path[i])
            else:
                Ns.append(good_path[i])

        reduced_cost = []
        for i in S:
            for j in graph[i]:
                if edge_cost[(i, j)] - vertex_cost[i] - vertex_cost[j] != 0:
                    reduced_cost.append(edge_cost[(i, j)] - vertex_cost[i] - vertex_cost[j])

        minprice = min(reduced_cost)

        for i in S:
            vertex_cost[i] += minprice
        for i in Ns:
            vertex_cost[i] -= minprice


good_paths = []

for i in range(len(matching)):
    for j in range(0, len(matching[i]) - 1):
        good_paths.append([matching[i][j], matching[i][j + 1]])


def xor_product(matching,good_path):
    global vertex_in_matching

    new_matching=[]
    for edge1 in good_path:
        counter=0

        for edge2 in matching :
            if (edge1[0],edge1[1])==(edge2[1],edge2[0]) or edge1==edge2  :
                counter+=1

                break
        if counter == 0 :
            new_matching.append(edge1)

    for edge1 in matching:
        counter=0
        for edge2 in good_path :
            if (edge1[0],edge1[1])==(edge2[1],edge2[0]) or edge1==edge2  :
                counter+=1
                break
        if counter == 0 :
            new_matching.append(edge1)
    return new_matching

matching = []
for i in good_paths:
    matching = xor_product(matching,[i])


foo_2 = open('out.txt','w')

sum_of_perfect_matching = 0
for i in range(len(matching)):
    foo_2.write(str(matching[i][0])+' '+str(matching[i][1])+' '+str(edge_cost[(matching[i][0], matching[i][1])])+'\n')
    print(matching[i][0],' ',matching[i][1],' ', edge_cost[(matching[i][0], matching[i][1])])
    sum_of_perfect_matching += edge_cost[(matching[i][0], matching[i][1])]
foo_2.write(str(sum_of_perfect_matching))
print(sum_of_perfect_matching)


#print(matching)
usable=matching
for i in usable:
    for j in range(len(i)):
        if i[j]>len(usable):
            i[j]-=len(usable)

for i in usable:
    for j in range(len(i)):
        i[j]-=1


# takes input from the file and creates a weighted bipartite graph
def CreateGraph():
    B = nx.Graph();
    f = open('inputvisual.txt')
    n = int(f.readline())
    cost = []

    for i in range(n):
        list1 = map(int, (f.readline()).split())
        cost.append(list1)

    people = []
    for i in range(n):
        people.append(i)
    job = []
    for c in ascii_lowercase[:n]:
        job.append(c)
    B.add_nodes_from(people, bipartite=0)  # Add the node attribute "bipartite"
    B.add_nodes_from(job, bipartite=1)
    for i in range(n):
        for c in ascii_lowercase[:n]:
            if cost[i][ord(c) - 97] > 0:
                B.add_edge(i, c, length=cost[i][ord(c)-97])
    return B, cost


def DrawGraph(B):
    global usable
    l, r = nx.bipartite.sets(B)
    pos = {}
    # Update position for node from each group
    pos.update((node, (1, index)) for index, node in enumerate(l))
    pos.update((node, (2, index)) for index, node in enumerate(r))
    nx.draw(B, pos, with_labels=True)  # with_labels=true is to show the node number in the output graph
    edge_labels = dict([((u, v), d['length']) for u, v, d in B.edges(data=True)])

    nx.draw_networkx_edge_labels(B, pos, edge_labels=edge_labels, label_pos=0.85,
                             font_size=6)  # prints weight on all the edges
    for i in usable:
        nx.draw_networkx_edges(B, pos, edgelist=[(i[0], chr(i[1] + 97) )], width=2.5, alpha=0.6, edge_color='r')
    return pos

if __name__ == "__main__":
    B, cost = CreateGraph();
    pos = DrawGraph(B)
    plt.show()


