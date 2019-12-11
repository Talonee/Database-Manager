import numpy as np
from matplotlib import pyplot as plt

# 16-pound bowling ball

g = 9.8 # gravity acc. constant (m/s^2)
m = 7.26 # mass of bowling (kg)
r = 0.11 # radius of bowling (m)
D = 0.5 # drag coefficient 
A = 0.038 # cross-sect area (m^2)
p = 1.225 # density (kg/m^3)

v = [0] * 40 # initialize a list of velocity

# create an evenly spaced sequence of time
# t = np.linspace(0, 12, 12*3) 

h = 0.3 # step size

for i in range(1, 40): # Velocity vs. Time
    v[i] = v[i-1] + (g-(D*A*p*np.square(v[i-1]))/(2*m))*h


for i in range(1, 12): # Velocity at each second
    a = round(v[i], 3)
    b = round(np.sqrt((2*m*g)/(D*p*A))*np.arctan(np.sqrt((D*p*A*g)/(2*m))*(h*i)), 3)
    print("Computation: {}\nActual: {}".format(a, b))
    print("% Error: ", round((a-b)/b*100, 3))
    print("-----")


# plt.plot(t, v, '-')
# plt.xlabel("Time")
# plt.ylabel("Velocity")
# plt.title("Computational Model: Velocity vs. Time")
# plt.show()



# g = 9.8 # gravity acc. constant (m/s^2)
# m = 1 # mass of sphere (kg)
# k = 0.1 # air resistance (kg/sec)

# v = [0] * 11 # initialize a list of velocity

# # create an evenly spaced sequence of time
# t = np.linspace(0, 12, 11) 

# h = 0.3 # step size

# # create the left hand side of the differential equation
# fxn = lambda y: g-(k/m)*np.square(y)

# for i in range(1, len(t)): # Velocity vs. Time
#     v[i] = v[i-1] + h*fxn(v[i-1])

# plt.plot(t, v, '-')
# plt.xlabel("Time")
# plt.ylabel("Velocity")
# plt.title("Approximate Solution with Euler's Method")
# plt.show()


