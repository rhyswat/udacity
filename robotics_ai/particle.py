# In this exercise, try to write a program that
# will resample particles according to their weights.
# Particles with higher weights should be sampled
# more frequently (in proportion to their weight).

# Don't modify anything below. Please scroll to the 
# bottom to enter your code.

from math import *
import random

landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0

class robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0;
        self.turn_noise    = 0.0;
        self.sense_noise   = 0.0;
    
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= world_size:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
    
    
    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise    = float(new_t_noise);
        self.sense_noise   = float(new_s_noise);
    
    
    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z
    
    
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'         
        
        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi
        
        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size    # cyclic truncate
        y %= world_size
        
        # set particle
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res
    
    def Gaussian(self, mu, sigma, x):
        
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    
    def measurement_prob(self, measurement):
        
        # calculates how likely a measurement should be
        
        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))



def eval(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))

#-------------------------------------------------------

# Make N particles and a robot
N = 1000
def initialise() :
    # return a list of particles and a robot object
    p = []
    for i in range(N):
        x = robot()
        x.set_noise(0.05, 0.05, 5.0)
        p.append(x)
    return p, robot()

# compute the similarity weighgts for a list of particles and measurement Z
def compute_weights(p, Z) :
    return [r.measurement_prob(Z) for r in p]

# Resample by cumulative dist. fn.
import bisect
def resample_by_cumulative(alphas):
    # this method is O(N log N) for N samples
    cumulative = []
    tot = 0
    for i in xrange(N) :
        tot += alphas[i]
        cumulative.append(tot)
    samples = []
    for i in xrange(N) :
        r = random.random()
        j = bisect.bisect_left(cumulative, r)
        samples.append(p[j])
    return samples

# The class Wheel example
def resample_by_wheel(weights) :
    # this method is O(N) for N samples
    wmax = max(weights)
    index = random.randint(0, N-1)
    beta = 0.0
    samples = []
    for i in xrange(N) :
        beta += random.uniform(0, 2*wmax)
        while weights[index] < beta:
            beta -= weights[index]
            index = (index + 1) % N
        samples.append(p[index])
    return samples

## The algorithm is based on the fact that, after sorting N uniformly distributed samples,
## the distances between two consecutive samples is exponentially distributed
## The algorithm is similar to the resampling wheel algorithm, except that it makes 
## exactly one revolution around the resampling wheel. 
## This resampling algorithm is O(N)
## http://forums.udacity.com/questions/3001328/an-on-unbiased-resampler#cs373
def resample_wheel_once(p, w):
    N = len(p)
    p3 = []
    #Instantiate diffs to store the distance between two consecutive samples
    diffs = range(N) 
    #select N numbers exponentially distributed with parameter lambda = 1
    for i in range(N):
        diffs[i] = -log(random.random())
    # stretch to fit the circumference of the resampling wheel
    scale = sum(w) / sum(diffs) 
    index = 0;
    beta = -random.random() * diffs[0] * scale #randomize the starting position
    # This for-loop does exactly one revolution around the resampling wheel
    for i in range(N):
        beta += diffs[i] * scale
        # The total number of iterations of this while-loop, summed over all iterations 
        # of the enclosed for-loop, is bounded by N-1
        while beta > w[index]:
            beta -= w[index]
            index += 1 # no need for %N since once around
        p3.append(p[index])
    return p3


# the sampling function I use
sample = resample_wheel_once

#-------------------------------------------------------
# run the whole lot a few times
p, myrobot = initialise()
ntimes = 10
print eval(myrobot, p)
for i in xrange(ntimes) :
    myrobot = myrobot.move(0.1, 0.5)
    Z = myrobot.sense()
    w = compute_weights(p, Z)
    p = sample(p, w)
    print eval(myrobot, p)

#-------------------------------------------------------
