colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

# rows, columns
R = len(colors)
C = len(colors[0])

def initialise(v=R*C) :
    # Creates a RxC table filled with V
    return [[v for c in range(C)] for r in range(R)]

def sense(p, Z) :
    q = initialise(0.0)
    s = 0 # sum(q) for normalising
    for r in xrange(R) :
        for c in xrange(C) :
            # this lot is the non-normalised Bayesian likelihood * prior == P(Z|X)P(X)
            likelihood = Z == colors[r][c] and sensor_right or (1-sensor_right)
            q[r][c] = p[r][c] * likelihood
            s += q[r][c]
    # normalise
    for r in xrange(R) :
        for c in xrange(C) :
            q[r][c] /= s    
    return q

def move (p, dr, dc) :
    """This is done by total probability: P(Xt+1) = Sum (P(Xt) * P(move from Xt))"""
    q = initialise(0.0)
    for r in xrange(R) :
        for c in xrange(C) :
            q[r][c] = (p[(r-dr)%R][(c-dc)%C] * p_move) + (p[r][c] * (1-p_move))
    # total prob -> no need for normalising
    return q

p = initialise()
show(p)
for (motion, measurement) in zip(motions, measurements):
    # NOTE!! The udacity assignment only works if you do move first,
    # despite the course notes and common sense say sense first.
    p = move(p, *motion)
    p = sense(p, measurement)

def max_cell(p) :
    rr = cc = b = -1
    for r in xrange(R) :
        for c in xrange(C) :
            if p[r][c] > b :
                rr = r
                cc = c
                b = p[r][c]
    return (rr, cc, b)
r, c, b = max_cell(p)
print ''
print 'The maximum probability is attained in row {}, column {}, p={}'.format(r+1, c+1, b)

#Your probability array must be printed 
#with the following code.
show(p)
