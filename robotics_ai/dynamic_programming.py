# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 17:16:07 2014

@author: RhysWatkin
"""

# ----------
# User Instructions:
# 
# Create a function compute_value() which returns
# a grid of values. Value is defined as the minimum
# number of moves required to get from a cell to the
# goal. 
#
# If it is impossible to reach the goal from a cell
# you should assign that cell a value of 99.

# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# insert code below
# ----------------------------------------

def compute_value():
    x_max = len(grid)
    y_max = len(grid[0])
    value = [[99] * y_max for x in xrange(x_max)] ## 99 -> inaccessible

    # like 'search' back from 'goal' until we visit every accessible node   
    import heapq 
    value[goal[0]][goal[1]] = 0
    open_list = [(0, goal[0], goal[1])]
    heapq.heapify(open_list)
    marked = set()
    while len(open_list) > 0 :
        v, x, y = heapq.heappop(open_list)
        marked.add((x,y))
        for d in delta :
            xx, yy = x + d[0], y + d[1]
            p = (xx, yy)
            if (p not in marked) and 0<=xx and xx<x_max and 0<=yy and yy<y_max and grid[xx][yy] == 0 :
                value[xx][yy] = v + cost_step
                heapq.heappush(open_list, (v+1, xx, yy))

    return value #make sure your function returns a grid of values as demonstrated in the previous video.

def optimum_policy(value) :
    # pass in the value table from 'value'
    x_max = len(grid)
    y_max = len(grid[0])
    policies = [[' '] * y_max for x in xrange(x_max)]
    
    # possibly to do with d/dx and d/dy of the values???
    
    # finally mark the goal with a '*'
    policies[goal[0]][goal[1]] = '*'
    
    
    return policies

value = compute_value()
policies = optimum_policy(value)
for v in policies :
    print v
