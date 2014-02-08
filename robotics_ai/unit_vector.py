import math

def length(vec) :
    return math.sqrt(sum(x*x for x in vec))

def normalise(vec) :
    n = length(vec)
    return [x/n for x in vec]

r1 = [0, 0, 0]

L = 5

# angles in radians
pitch = math.pi/4
yaw = math.pi/4
r_unit = normalise([math.cos(yaw) * math.cos(pitch), \
                    math.sin(yaw) * math.cos(pitch), \
                    math.sin(pitch)])

r2 = [r1[0] + L*r_unit[0],\
      r1[1] + L*r_unit[1],\
      r1[2] + L*r_unit[2]]

print r2
print length(r2)
