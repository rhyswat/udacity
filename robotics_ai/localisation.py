#Given the list motions = [1,1] which means the robot 
#moves right and then right again, compute the posterior 
#distribution if the robot first senses red, then moves 
#right one, then senses green, then moves right again, 
#starting with a uniform prior distribution.

# initial prior is uniform
p = [0.2, 0.2, 0.2, 0.2, 0.2]
world = ['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
motions = [1,1]
pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

# Sensing: P(x|Z) = P(x)*P(Z = actual state of the world)
def sense(p, Z):
    q = []
    for i in range(len(p)):
        hit = (Z ==  world[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s = sum(q)
    for i in range(len(q)):
        q[i] = q[i] / s
    return q

def move(p, U):
    q = []
    for i in range(len(p)):
        s = pExact * p[(i-U) % len(p)]
        s = s + pOvershoot * p[(i-U-1) % len(p)]
        s = s + pUndershoot * p[(i-U+1) % len(p)]
        q.append(s)
    return q


# assume num motions = num measurements
# then iterate sense>moves>sense>move>...
for i in xrange(len(measurements)) : 
    p = sense(p, measurements[i])
    p = move(p, motions[i])

# the most likely location of the robot is the index with max probability
def argmax(p) :
    best_index, best = -1, -1
    for i in xrange(len(p)) :
        if p[i] > best :
            best = p[i]
            best_index = i
    return best_index, best

likely_cell, likely_prob = argmax(p)
print 'The robot is most likely at cell {} of {} with probability {}'.format(likely_cell+1, len(p), likely_prob)
print 'Distribution:'
for i in xrange(len(p)) :
    print ' cell {} :: {}'.format(i+1, p[i])
