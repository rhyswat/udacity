# ----------------
# User Instructions
#
# Implement twiddle as shown in the previous two videos.
# Your accumulated error should be very small!
#
# Your twiddle function should RETURN the accumulated
# error. Try adjusting the parameters p and dp to make
# this error as small as possible.
#
# Try to get your error below 1.0e-10 with as few iterations
# as possible (too many iterations will cause a timeout).
# No cheating!
# ------------
 
from math import *
import random


# ------------------------------------------------
# 
# this is the robot class
#

class robot:

    # --------
    # init: 
    #    creates robot and initializes location/orientation to 0, 0, 0
    #

    def __init__(self, length = 20.0):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    # --------
    # set: 
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)


    # --------
    # set_noise: 
    #	sets the noise parameters
    #

    def set_noise(self, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # set_steering_drift: 
    #	sets the systematical steering drift parameter
    #

    def set_steering_drift(self, drift):
        self.steering_drift = drift
        
    # --------
    # move: 
    #    steering = front wheel steering angle, limited by max_steering_angle
    #    distance = total distance driven, most be non-negative

    def move(self, steering, distance, 
             tolerance = 0.001, max_steering_angle = pi / 4.0):

        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0


        # make a new copy
        res = robot()
        res.length         = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.steering_drift = self.steering_drift

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = tan(steering2) * distance2 / res.length

        if abs(turn) < tolerance:

            # approximate by straight line motion

            res.x = self.x + (distance2 * cos(self.orientation))
            res.y = self.y + (distance2 * sin(self.orientation))
            res.orientation = (self.orientation + turn) % (2.0 * pi)

        else:

            # approximate bicycle model for motion

            radius = distance2 / turn
            cx = self.x - (sin(self.orientation) * radius)
            cy = self.y + (cos(self.orientation) * radius)
            res.orientation = (self.orientation + turn) % (2.0 * pi)
            res.x = cx + (sin(res.orientation) * radius)
            res.y = cy - (cos(res.orientation) * radius)

        return res




    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)


# ------------------------------------------------------------------------
#
# run - does a single control run.

def run(params, printflag=False):
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0)
    myrobot.set_steering_drift(radians(10))
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    dt = 1.0
    N = 100
    #
    # Enter code here
    #

    P,D,I = params
    xtrack_error = myrobot.y
    integral = 0.0
    err = 0.0
    for i in xrange(N*2) : # only accumulate error for i>=N
        # d/dt, remembering previous
        differential = (myrobot.y - xtrack_error)/dt
        xtrack_error =  myrobot.y

        # integral term
        integral += xtrack_error*dt

        # update & print
        steering = -P*myrobot.y - I*integral - D*differential
        myrobot = myrobot.move(steering, dt*speed)

        if i >= N :
            err += (xtrack_error**2)
        if printflag :
            print myrobot, steer

    # Returns the average error so far
    return err / N

# ------------------------------------------------------------------
def twiddle(tol = 0.001):
    """
    Coordinate ascent / descent, a form of local hill climbing
    http://en.wikipedia.org/wiki/Coordinate_descent

    Really relies on the cost function run(params) being smooth & well behaved

    Also it's really sensitive to the direction of hill climbing.
    Since the paramter vector is initialised to 0 then the order of the
    parameters is arbitrary. But this sets the search off in different
    directions and therefore finds different local minima.
    The code passes the assignment if p=(P,D,I) but not if P=(P,I,D)...
    """
    num_params = 3
    p =  [0.0] * num_params
    dp = [1.0] * num_params
    #dp[2] = 0 # switch off the ith term
    
    best = run(p)
    err = 0.0
    while sum(dp) > tol :
        for i in xrange(num_params) :
            p[i] += dp[i]
            err = run(p)
            if err < best :
                # good, keep climbing upwards
                best = err
                dp[i] *= 1.1
            else :
                # try climbing down (1 to original, 1 to go down)
                p[i] -= 2*dp[i] 
                err = run(p)
                if err < best :
                    # good, keep climbing down
                    best = err
                    dp[i] *= 1.1
                else :
                    # revert to original and reduce dp
                    p[i] += dp[i]
                    dp[i] *= 0.9
    return p

params = twiddle(1e-3)
err = run(params)
print 'Final params:', params, '\n ->', err

