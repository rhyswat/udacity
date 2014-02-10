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

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

heuristic = [[9, 8, 7, 6, 5, 4],
            [8, 7, 6, 5, 4, 3],
            [7, 6, 5, 4, 3, 2],
            [6, 5, 4, 3, 2, 1],
            [5, 4, 3, 2, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

# ----------------------------------------
# modify code below
# ----------------------------------------

def search():
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    
    # action list: {node:(parent, action taken at 'node')}
    actions = {tuple(init): (None, None)}

    x = init[0]
    y = init[1]
    g = 0

    def heuristic_fn(x, y) :
        return heuristic[x][y]

    def h2(x,y) :
        return abs(x - goal[0]) + abs(y - goal[1])

    open_list = [[g + h2(x, y), g, x, y]]

    found = False  # flag that is set when search is complete
    resign = False # flag set if we can't find expand
    count = 0
    
    while not found and not resign:
        if len(open_list) == 0:
            resign = True
            return "Fail"
        else:
            open_list.sort()
            open_list.reverse()
            current = open_list.pop()
            f, g, x, y = current
            expand[x][y] = count
            count += 1
            
            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            open_list.append([g2 + heuristic_fn(x2, y2), g2, x2, y2])
                            closed[x2][y2] = 1
                            actions[(x2, y2)] = ((x,y), i)
    for i in range(len(expand)):
        print expand[i]
        
    # make the funky path depiction
    node, action = tuple(goal), None
    path = []
    while node is not None and actions.has_key(node) :
        x,y = node
        path.append((node,action))
        node, action = actions[node]
    path.reverse()
    print ''
    print 'Path:'
    print " -> ".join([str(z) for z in path])

    visual_path = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    for x in range(len(grid)) :
        for y in range(len(grid[0])) :
            if grid[x][y] == 1 :
                visual_path[x][y] = '*' # obstacle
    for n,a in path :
        x,y = n
        s = a is None and 'G' or delta_name[a]
        visual_path[x][y] = s
    visual_path[init[0]][init[1]] = 'S'
    for v in visual_path :
        print v
    
        
    return expand #Leave this line for grading purposes!

search()



