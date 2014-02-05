# Find Eulerian Tour
#
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]

import collections

def get_edges(g, u) :
    return [e for e in g if (e[0] == u or e[1] == u)]

def get_next(graph, u) :
    edges = get_edges(graph, u)
    if len(edges) == 0 :
        print 'Nowhere to go from {} -- returning'.format(u)
        return None
    edge = edges[0]
    graph.remove(edge)
    v = edge[0] == u and edge[1] or edge[0]
    print 'adding {}->{}'.format(u,v)
    return v

def follow(graph, start) :
    path = [start]
    v = get_next(graph, start)
    while v is not None :
        path.append(v)
        if v != start :
            v = get_next(graph, v)
        else :
            break
    return path

def hierholzer(g) :
    graph = list(g)
    visited = set()
    u = graph[0][0]
    tour = follow(graph, u)
    print 'Initial tour from {} :: {}'.format(u, tour)
    visited.update(set(tour))
    remaining = [(u, get_edges(graph, u)) for u in visited]
    remaining = [ x for x in remaining if len(x[1]) > 0]
    while len(remaining) > 0 :
        u, e = remaining.pop()
        tt = follow(graph, u)
        print 'Mini tour from {} :: {}'.format(u, tt)
        visited.update(set(tt))
        # insert tt into the tour
        i = tour.index(u)
        tour = tour[0:i] + tt + tour[i+1:]
        remaining = [(u, get_edges(graph, u)) for u in visited]
        remaining = [ x for x in remaining if len(x[1]) > 0]
    return tour

def find_eulerian_tour(graph):
    # your code here
    return hierholzer(graph)

graphs = []
graphs.append([(1, 2), (2, 3), (3, 1)])

graphs.append([(0, 1), (1, 5), (1, 7), (4, 5),\
               (4, 8), (1, 6), (3, 7), (5, 9),\
               (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)])

graphs.append([(1, 13), (1, 6), (6, 11), (3, 13), \
               (8, 13), (0, 6), (8, 9),(5, 9), \
               (2, 6), (6, 10), (7, 9),(1, 12), \
               (4, 12), (5, 14), (0, 1),  (2, 3), \
               (4, 11), (6, 9),(7, 14),  (10, 13)])  


graphs.append([(8, 16), (8, 18), (16, 17), (18, 19),\
               (3, 17), (13, 17), (5, 13),(3, 4), \
               (0, 18), (3, 14), (11, 14), (1, 8), \
               (1, 9), (4, 12), (2, 19),(1, 10), (7, 9), \
               (13, 15), (6, 12), (0, 1), (2, 11), (3, 18), \
               (5, 6), (7, 15), (8, 13), (10, 17)])

for g in graphs :
    print ''
    print '-----------------------------------'
    print hierholzer(g)

