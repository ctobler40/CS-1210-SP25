# I am making the case for 2 functions. One has weights and one does not. 
# One is a CSV and one is not. different format so hard to do one function
# without doing some crazy hack. Just provide the correct one as the solution 
# is the better approach IMHO
def loadNetwork_txt():
    with open('soc-Epinions1.txt', 'r') as file:
        in_neighbors = {}
        out_neighbors = {}
        for line in file: #iterate over lines of files
            if not (line[0] == '#'): # lines starting with '#' are comments, ignore those
                source,dest = line.split()
                in_l = in_neighbors.get(dest,[]) # get or defualt the empty list
                in_l.append(source) # add a to the adj. list
                in_neighbors[dest] = in_l
                out_l = out_neighbors.get(source,[]) #do the same for out_neighbors
                out_l.append(dest)
                out_neighbors[source] = out_l
                #no weights on this graph!
    res = [in_neighbors, out_neighbors]
    return res

def loadNetwork_csv():
    with open('soc-sign-bitcoinotc.csv', 'r') as file:
        in_neighbors = {}
        out_neighbors = {}
        weights = {} #maps f"{source}:{dest}" to the weight
        for line in file: #iterate over lines in the file
            source, dest, weight, timestamp = line.split(',') # get everything but ignore the timestamp
            in_l = in_neighbors.get(dest,[]) # get or defualt the empty list
            in_l.append(source) # add a to the adj. list
            in_neighbors[dest] = in_l
            out_l = out_neighbors.get(source,[]) #do the same  for out_neighbors
            out_l.append(dest)
            out_neighbors[source] = out_l
            weight_str = f"{source}:{dest}" #note that this is directed from the specification. 
            #The same weight does not exist for f"{dest}:{source}"
            weights[weight_str] = weight
        res = res = [in_neighbors, out_neighbors,weights] #create the graph and return it
        return res

def getActiveNeighbors(graph, node: str, activeSet:set):
    # I assume that you pass in an instance of my graph object
    res = set()
    in_edges = graph[0].get(node, []) # get all the nodes that have an edge to this node
    for node in in_edges: 
        if node in activeSet: 
            res.add(node)
    return res


# Simulating the Linear Threshold Model for Information Spread on a network
# args: G = (V, E, w). Presuming a graph with Vertices, Edges, and weights assigned to each
# Each Vetice is to have some linear threshold T e {0, 1}, representing the amount needed for the Vertice to become "active"
# The algorithm stops when there is an iteration in which the active set does NOT grow
def simulateLinearThreshold(graph, activeSet:set):
    # Unpack our graph components
    in_neighbors, out_neighbors, weights = graph
    # Iterate through all of our nodes in the graph
    for node in in_neighbors:
        # For checking theshold (For now, all thresholds are presumably 1 for each node)
        # Suggestion: Calculate the threshold based on the number of active neighbors and number of total neighbors?
        # Basically, nodes that have less active neighbors are less likely to become active themselves?
        node_threshold = 1
        active_length = len(activeSet)
        # Get all of the nodes that share and edge with the node we are currently checking
        share_edge = in_neighbors.get(node, [])
        # Now iterate through these nodes and see if their weights are more than the threshold
        for shared_node in share_edge:
            if shared_node in activeSet:
                # If it is an active node, we subtract the weight from the threshold
                weight_key = f"{shared_node}:{node}"
                weight = float(weights.get(weight_key, 0))
                node_threshold = max(0, node_threshold - weight)
                if (node_threshold == 0):
                    # If it reaches 0, we now move the node to the active set
                    activeSet.add(node)
                    break
        # If the active set does not grow, we stop the iteration
        if len(activeSet) == active_length:
            break
    # Return the updated set
    # If this function cannot take activeSet as an extra argument, we could also update some global active set
    return activeSet


# Everything below is for testing
#graph_csv = loadNetwork_csv()
#activeSet = set([str(n) for n in range(1, 3001)])
#print(len(activeSet))
#simulateLinearThreshold(graph_csv, activeSet)
#print(len(activeSet))

#print("\nCSV-based Graph (With Weights):")
#print("In Neighbors:", graph_csv[0]['2'])
#print("Out Neighbors:", graph_csv[1]['2'])
#print("Weights:", graph_csv[2]['2'])

# Load the text-based network without weights
#graph_txt = loadNetwork_txt()
#print("Text-based Graph (No Weights):")
#print("In Neighbors:", graph_txt[0])
#print("Out Neighbors:", graph_txt[1])

# Load the CSV-based network with weights
#graph_csv = loadNetwork_csv()
#print("\nCSV-based Graph (With Weights):")
#print("In Neighbors:", graph_csv[0])
#print("Out Neighbors:", graph_csv[1])
#print("Weights:", graph_csv[2])

# Test getActiveNeighbors function with a sample active set
# Assuming we want to check active neighbors for node '3' with '1' as active in activeSet
#activeSet = set([str(n) for n in range(1, 1001)])
#active_neighbors_txt = getActiveNeighbors(graph_txt, '65', activeSet)
#print("\nActive Neighbors in Text-based Graph for Node 65:", active_neighbors_txt)

#active_neighbors_csv = getActiveNeighbors(graph_csv, '65', activeSet)
#print("Active Neighbors in CSV-based Graph for Node 65:", active_neighbors_csv)
