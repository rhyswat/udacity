# -----------
# User Instructions:
#
# Modify the the search function so that it becomes
# an A* search algorithm as defined in the previous
# lectures.
# ----------

import math
import heapq

# grid is indexed [x][y] strangely
grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
x_max = len(grid) - 1
y_max = len(grid[0]) - 1

# initial and goal state
init = [0, 0]
goal = [x_max, y_max]

# robot actions, assumed to always complete successfully
delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

# step cost for each action
cost = 1

# ----------------------------------------
# visualisation helpers
# ----------------------------------------
def print_expansions(expand) :
    e = max(max(i) for i in expand)
    print ''
    print 'Expansions (max={}):'.format(e)
    print '* = obstacle, ? = not visited, n = order of visit'

    for x in xrange(len(expand)) :
        r = []
        for y in xrange(len(expand[x])) :
            if grid[x][y] == 1 :
                r.append('   *')
            elif expand[x][y] == -1 :
                r.append('   ?')
            else :
                r.append('%4d' % expand[x][y])
        print ' '.join(r)
    
def print_grid() :
    for g in grid :
        print g

def build_path(actions) :
    node, action = tuple(goal), None
    path = []
    while node is not None and actions.has_key(node) :
        x,y = node
        path.append((node,action))
        node, action = actions[node]
    path.reverse()
    return path

def print_path(path) :
    print ''
    print 'Path: ({} steps)'.format(len(path)-1) # -1 as the path is the list of nodes not steps
    if len(path) > 0 :
        print '\n-> '.join([str(n) for n,a in path])

def print_route(path) :
    print ''
    print 'Path taken:'
    visual_path = [[' ' for row in range(len(grid[0])+2)] for col in range(len(grid)+2)]
    for x in range(len(visual_path)) :
        for y in range(len(visual_path[0])) :
            if (x == 0 and y == 0) \
               or (x == 0 and y == y_max+2) \
               or (x== x_max+2 and y == 0) \
               or (x == x_max+2 and y == y_max+2) :
                visual_path[x][y] = '+'
            elif x == 0 or x == x_max+2 :
                visual_path[x][y] = '-'
            elif y==0 or y == y_max+2 :
                visual_path[x][y] = '|'
            elif 1<=x and x <=x_max+1 and 1<=y and y<=y_max+1 and grid[x-1][y-1] == 1:
                visual_path[x][y] = '*'
    for n,a in path :
        x,y = n
        s = a is None and 'G' or delta_name[a]
        visual_path[x+1][y+1] = s
    visual_path[init[0]+1][init[1]+1] = 'S'
    for v in visual_path :
        print ' '.join(v)    

# ----------------------------------------
# a*-search
# ----------------------------------------
# the heuristic functions
def l_infinity(x, y) :
    return min(abs(x - goal[0]), abs(y - goal[1]))
def manhattan(x, y) :
    return abs(x - goal[0]) + abs(y - goal[1])
def euclidian(x, y) :
    return math.hypot(x - goal[0], y - goal[1])
def zero(x, y) :
    return 0

# This is breadth first
def search(heuristic=zero):
    # ----------------------------------------------------------------------
    # expand[x][y] is the step at which xy was visited
    # -1 means never visited (which might be a good thing)
    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    count = 0

    # ----------------------------------------------------------------------
    # visited nodes
    marked = set()
    def mark(x, y) :
        marked.add((x,y))
  
    # ----------------------------------------------------------------------
    # action list records how we got to 'node' from its parent
    #        a[node] = (parent node, action taken to get from parent to node)}
    # can reverse-engineer the path from start to goal from this.
    actions = {tuple(init): (None, None)}

    # ----------------------------------------------------------------------
    # the heuristic functions
    print 'Heuristic function:',heuristic.__name__

    # ----------------------------------------------------------------------
    # the exploration front: (f = g + h(x,y), g, x, y)
    open_list = []
    def push(g, x, y) :
        heapq.heappush(open_list, (g + heuristic(x,y), g, x, y))

    push(0, *init)
    mark(*init)
    found = False
    while len(open_list) > 0:
        # heuristic (ignored inside the loop), cost so far, x and y
        h, g, x, y = heapq.heappop(open_list)

        # update the expansion table 
        expand[x][y] = count
        count += 1

        # are we at the goal?
        if x == goal[0] and y == goal[1] :
            found = True
            break

        # expand this location
        for i in xrange(len(delta)) :
            d = delta[i]
            p = (x + d[0], y + d[1])
            if p not in marked \
               and 0 <= p[0] and p[0] <= x_max \
               and 0 <= p[1] and p[1] <= y_max \
               and grid[p[0]][p[1]] != 1 :
                # p is reachable :-)
                g2 = g + cost           # path cost without heuristic
                push(g2, *p)            # add to the open list
                mark(*p)                # mark as visited
                actions[p] = ((x,y), i) # record how we got here

    if not found :
        print '** FAILED **'
        print '   No route from {} to {} in this grid'.format(init, goal)
        print_grid()
        return None
    
    # ok :-) -- build the path from the action records
    path = build_path(actions)
    
    # visualisation ------------------------------------------------
    print_expansions(expand)
    print_path(path)
    print_route(path)
    # --------------------------------------------------------------

    return path

if __name__ == '__main__' :
    path = search(manhattan)



