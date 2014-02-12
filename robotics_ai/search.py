# -----------
# User Instructions:
#
# Modify the the search function so that it becomes
# an A* search algorithm as defined in the previous
# lectures.
#
# Your function should return the expanded grid
# which shows, for each element, the count when
# it was expanded or -1 if the element was never expanded.
# In case the obstacles prevent reaching the goal,
# the function should return "Fail"
#
# You do not need to modify the heuristic.
# ----------

# grid is indexed [x][y] oddly
grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
x_max = len(grid) - 1
y_max = len(grid[0]) - 1

# initial and goal state
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

# robot actions, assumed to always complete successfully
delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

# ----------------------------------------
# helpers
# ----------------------------------------
def print_expansions(expand) :
    print ''
    print 'Expansions table'
    for i in range(len(expand)):
        print ' '.join(['  %2d' %j for j in expand[i]])
    
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
    print ''
    print 'Path: ({} steps)'.format(len(path)-1) # -1 as the path is the list of nodes not steps
    if len(path) > 0 :
        print ' -> '.join([str(n) for n,a in path])
    return path

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
import heapq
def search():
    # ----------------------------------------------------------------------
    # expand[x][y] is the step at which xy was visited
    # -1 means never visited (which might be a good thing)
    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    count = 0

    # ----------------------------------------------------------------------
    # visited nodes
    marked = set()

    # ----------------------------------------------------------------------
    # action list: {node:(parent, action taken at 'node')}
    actions = {tuple(init): (None, None)}

    # ----------------------------------------------------------------------
    # the heuristic function    
    def heuristic(x,y) :
        return abs(x - goal[0]) + abs(y - goal[1])

    # ----------------------------------------------------------------------
    xx, yy = init
    open_list = [(heuristic(xx, yy), 0, xx, yy)]
    heapq.heapify(open_list)
    found = False
    while len(open_list) > 0:
        f, g, x, y = heapq.heappop(open_list)

        # are we at the goal?
        if x == goal[0] and y == goal[1] :
            expand[x][y] = count
            count += 1
            found = True
            break

        # this location is on the path if it's not visited
        location = (x,y)
        if location not in marked :
            expand[x][y] = count
            count += 1
            marked.add(location)
            for i in xrange(len(delta)) :
                d = delta[i]
                p = (x + d[0], y + d[1])
                if p not in marked \
                   and 0 <= p[0] and p[0] <= x_max \
                   and 0 <= p[1] and p[1] <= y_max \
                   and grid[p[0]][p[1]] != 1 :
                    g2 = g + cost
                    heapq.heappush(open_list, (g2 + heuristic(*p), g2, p[0], p[1]))
                    actions[p] = ((x,y), i)

    if not found :
        print '** FAILED **'
        print '   No route from {} to {} in this grid'.format(init, goal)
        print_grid()
        return 'fail'
    
    # -- visualisation -------------------------------------------------
    # otherwise...
    # show the expansions
    print_expansions(expand)
        
    # make the funky path depiction
    path = build_path(actions)

    # print a visual grid with a bounding edge
    print_route(path)
    # ----------------------------------------------------------------------
    
        
    return expand #Leave this line for grading purposes!

search()



