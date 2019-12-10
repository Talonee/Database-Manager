# import numpy as np
# from matplotlib import pyplot as plt

# g = 9.8 # gravity acc. constant (m/s^2)
# m = 1 # mass of sphere (kg)
# k = 0.1 # air resistance (kg/sec)

# v = [0] * 1001 # initialize a list of velocity

# # create an evenly spaced sequence of time
# t = np.linspace(0, 10, 1001) 

# h = t[2] - t[1] # step size

# # Create the left hand side of the differential equation
# fxn = lambda y: g-(k/m)*np.square(y)

# for i in range(1, len(t)): # Euler
#     v[i] = v[i-1] + h*fxn(v[i-1])

# plt.plot(t, v, '-')
# plt.xlabel("Time")
# plt.ylabel("Velocity")
# plt.title("Approximate Solution with Euler's Method")
# plt.show()

import numpy as np
from matplotlib import pyplot as plt

g = 9.8 # gravity acc. constant (m/s^2)
m = 7.26 # mass of sphere (kg)
d = 0.5 # drag coefficient
p = 1.225 # density (kg/m^3)
a = 0.038 # cross-sectional area (m^2)

v = [0] * 1001 # initialize a list of velocity

# create an evenly spaced sequence of time
t = np.linspace(0, 10, 1001) 

h = t[5] - t[1] # step size

# Create the left hand side of the differential equation
# fxn = lambda y: g-(k/m)*np.square(y)
fxn = lambda y: np.sqrt(2*m*g/d/p/a)*np.arctan(np.sqrt(d*p*a*g/2/m)*y)

for i in range(1, len(t)): # Euler 2
    v[i] = v[i-1] + h*fxn(t[i-1])

plt.plot(t, v, '-')
plt.xlabel("Time")
plt.ylabel("Velocity")
plt.title("Approximate Solution with Euler's Method")
plt.show()