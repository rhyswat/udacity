import math

def gaussian(mu, sigma2, x) :
    return (1.0/math.sqrt(2*math.pi*sigma2))*math.exp(-0.5*(x-mu)*(x-mu)/sigma2)

# update from measurement:
# modify the location distribution mean1, var1 with
# the measured location mean2, var2
def update(mean1, var1, mean2, var2) :
    # Multiplies two Gaussans for the update step
    new_mean = (var2 * mean1 + var1 * mean2) / (var1 + var2)
    new_var = 1/(1/var1 + 1/var2)
    return (new_mean, new_var)

# predict from motion:
# modify the location distribution mean1, var1 with
# the movement with distribution mean2, var2
def predict(mean1, var1, mean2, var2) :
    # Adds two Gaussians for the prediction step
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return (new_mean, new_var)
    

measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0
sig = 10000

#Please print out ONLY the final values of the mean
#and the variance in a list [mu, sig]. 

# Insert code here
# pair up (measurements, motions), loop round update>predict
for measurement, movement in zip(measurements, motion) :
    mu, sig = update(mu, sig, measurement, measurement_sig)
    mu, sig = predict(mu, sig, movement, motion_sig)

print [mu, sig]
