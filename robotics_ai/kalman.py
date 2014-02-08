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
    

measurements = [5.0, 6.0, 7.0, 9.0, 10.0]
motion = [1.0, 1.0, 2.0, 1.0, 1.0]
# motion & measurement variances
measurement_sig = 4.0
motion_sig = 2.0
# initial data
mu = 0.0      # the initial position compared with measurements[0]
sig = 10000.0 # large -> very uncertain initially -> dominated by 1st measurement

#Please print out ONLY the final values of the mean
#and the variance in a list [mu, sig]. 

# Insert code here
# pair up (measurements, motions), loop round update>predict
for measurement, movement in zip(measurements, motion) :
    mu, sig = update(mu, sig, measurement, measurement_sig)
    mu, sig = predict(mu, sig, movement, motion_sig)

print [mu, sig]
