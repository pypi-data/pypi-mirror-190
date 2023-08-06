# this "Solving TSP with Integer Linear Program" python snippet was sourced by the site of Sandipanweb:
# https://sandipanweb.wordpress.com/2020/12/08/travelling-salesman-problem-tsp-with-python/

from mip import Model, xsum, minimize, BINARY
from itertools import product
import time

import xml.etree.ElementTree
import re
import geopy.distance
import matplotlib.pyplot as plt
import itertools
import networkx as nx
    
def TSP_ILP(G):
    
    start = time.time()
    V1 =  range(len(G))
    n, V = len(G), set(V1)
    model = Model()
    # binary variables indicating if arc (i,j) is used 
    # on the route or not
    x = [[model.add_var(var_type=BINARY)
    for j in V] for i in V] 
    # continuous variable to prevent subtours: each city will have a
    # different sequential id in the planned route except the 1st one
    y = [model.add_var() for i in V]   # objective function: minimize the distance
    model.objective = minimize(xsum(G[i][j]*x[i][j] \
    for i in V for j in V))
    
    # constraint : leave each city only once
    for i in V:
        model += xsum(x[i][j] for j in V - {i}) == 1   # constraint : enter each city only once
    for i in V:
        model += xsum(x[j][i] for j in V - {i}) == 1   # subtour elimination
    for (i, j) in product(V - {0}, V - {0}):
        if i != j:
            model += y[i] - (n+1)*x[i][j] >= y[j]-n   # optimizing
    model.optimize()   # checking if a solution was found
    if model.num_solutions:
        print('Total distance {}'.format(model.objective_value))
        nc = 0 # cycle starts from vertex 0
        cycle = [nc]
    while True:
        nc = [i for i in V if x[nc][i].x >= 0.99][0]
        cycle.append(nc)
        if nc == 0:
            break
     
    return (model.objective_value, cycle)
    

while True:
    try:
        namekml = input('Type the "name.kml" of the file:  ')
        # KML parse
        tree = xml.etree.ElementTree.parse(namekml)
        root = tree.getroot()
    except FileNotFoundError:
        print('something went wrong! Try again.')
    else:
        break

    
  # Identify default namespace
namespace = re.match('\{(.*?)\}kml', root.tag).group(1)
ns = {'def': namespace}
    
  # Define coordinates RegEx
coord_ex = '(-?\d+\.\d+),'
heig_ex = '(\d+)'
regex = coord_ex + coord_ex + heig_ex
      
coord_tab = []
nod_name = []
# Find coordinates
for i in root.findall('.//def:Placemark', ns):
    name = i.find('def:name', ns).text
    coord = i.find('.//def:coordinates', ns)
    nod_name.append(name)
    # Check for placeless placemark     
    if not coord is None:
        coord = coord.text.strip()
        coord = re.findall(regex, coord)
    # Save data
        for (long, lat, heig) in coord:      
            if i.find('.//def:Point', ns):
                coord_tab.append((float(lat), float(long)))
                
# create coordinates dictionary
n = len(coord_tab)
dict_coord = {i: {} for i in range(n)}
for i, j in itertools.combinations(range(n), 2):
    x1, y1 = coord_tab[i]
    x2, y2 = coord_tab[j]
    weight = geopy.distance.geodesic(coord_tab[i], coord_tab[j]).m
    dict_coord[i][j] = round(weight, 2)
    dict_coord[j][i] = round(weight, 2)

# Define the list of vertices and edges for the graph
vertices = list(range(n))

edges_temp = []
edges = []
for i in range(n):
    for j in range(n):
        if i!=j:
            edges_temp.append((nod_name[i],nod_name[j]))
        else:
            continue

for i in edges_temp:
    i_r = i[::-1] # reverse the element

    # check that it doesn't appear in the list, reversed or not... 
    if i_r not in edges and i not in edges:
        edges.append(i)


# Create a graph using NetworkX
G = nx.Graph()
G.add_nodes_from(nod_name)
G.add_edges_from(edges)

# Define the positions for each vertex
pos_lalo= dict(map(lambda i,j : (i,j) , nod_name, coord_tab))

#invert long / lat to plot points correctly
pos = {city:(long, lat) for (city, (lat,long)) in pos_lalo.items()}

def visualize_graph(dict_coord, pos):
    # Draw the graph using NetworkX
    nx.draw(dict_coord, pos, with_labels=True, node_color='skyblue',alpha=0.6, node_size=500, edge_color='grey', width=0.6)

    # Show the plot
    plt.show()
    
# Visualize the graph
visualize_graph(G, pos)

def create_input_graph(n):
    G = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            G[i][j] = round(geopy.distance.geodesic(coord_tab[i], coord_tab[j]).m,2)
            G[j][i] = G[i][j]
    return G

G = create_input_graph(n)

#create a variable to place the result suggested by TSP function
result = list(TSP_ILP(G))
xy = result.pop(1)

# print the result and export a .txt file
# with the coordinates of the tsp path
TSP_points = []
pas = list(pos_lalo.items())
for i in xy:
    TSP_points.append(coord_tab[i])
    print(pas[i])
    
print('The total distance is:', result, 'meters')

# input the name of the text file to be exported
while True:
    try:
        
        filename = input("Type the 'name.txt' of the file to export coordinates:  ")
        with open (filename, 'x') as f:
            f.write( '\n'.join(' '.join(str(x) for x in tu) for tu in TSP_points) )
        
    except FileExistsError:
        print( "\n This name already exists! Type something different. \n")
        continue
    else:
        break

#generate a graph with the TSP solution
tsp_edges = []
i = 1
while i in range(len(xy)):
    tsp_edges.append((nod_name[xy[i]],nod_name[xy[i-1]]))
    i+=1

G = nx.Graph()
G.add_nodes_from(nod_name)
G.add_edges_from(tsp_edges)

def visualize_graph(dict_coord, pos):
    # Draw the graph using NetworkX
    nx.draw(dict_coord, pos, with_labels=True, node_color='skyblue',alpha=0.6, node_size=500, edge_color='lightgreen', width=1)

    # Show the plot
    plt.show()


visualize_graph(G, pos)

