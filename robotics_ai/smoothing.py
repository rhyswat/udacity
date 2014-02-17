# -----------
# User Instructions
#
# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth)
# and returns a smooth path.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached. The update should be done according to the
# gradient descent equations given in the previous video:
#
# If your function isn't submitting it is possible that the
# runtime is too long. Try sacrificing accuracy for speed.
# -----------


from math import *

# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

# ------------------------------------------------
# smooth coordinates
#

def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance=0.00001):

    # Make a deep copy of path into newpath
    newpath = [[0 for col in range(len(path[0]))] for row in range(len(path))]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] = path[i][j]


    #### ENTER CODE BELOW THIS LINE ###
    d = len(newpath[0])
    change = tolerance
    iteration, limit = 1, 5000
    while change >= tolerance and iteration <= limit :
        change = 0
        for i in xrange(1,len(path)-1) :
            yi = newpath[i]
            old = tuple(yi)

            yi = [yi[j] + weight_data*(path[i][j] - yi[j]) for j in xrange(d)]

            yim = newpath[i-1]
            yip = newpath[i+1]
            yi = [yi[j] + weight_smooth*(yim[j] - 2*yi[j] + yip[j]) for j in xrange(d)]
            newpath[i] = yi

            change += sum(abs(yi[j] - old[j]) for j in xrange(d))

        print '{:4f}: change={:.6f}'.format(iteration, change)
        iteration += 1
        
    
    return newpath # Leave this line for the grader!

# feel free to leave this and the following lines if you want to print.
newpath = smooth(path)

# thank you - EnTerr - for posting this on our discussion forum
for i in range(len(path)):
    print '['+ ', '.join('%.3f'%x for x in path[i]) +'] -> ['+ ', '.join('%.3f'%x for x in newpath[i]) +']'





