import numpy as np
from numpy import genfromtxt

rewards = np.array([0,0,0,0,0,0,0,-1,1])

values=  np.array([
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
])

print(values+rewards)

PT = genfromtxt('test.csv', delimiter=',')
print(PT.shape)

MAX_ITERS = 100
tolerance = 0.01

for it in range(MAX_ITERS):
    print("iteration: ", it+1)
    values_new = np.matmul(PT, values) + rewards
    if np.allclose(values_new, values, atol=tolerance, rtol=0):
        break
    values = values_new

values = np.round(values, 3)
print(values)


# PART 1

import numpy as np
from numpy import genfromtxt

rewards = np.array([
    1,
    -2,
    -2,
    -2,
    -2,
    -2,
    -2,
    -2,
    -2,
    -2,
    -2,
    -2,
    -2,
    -2,
    -2,
    1
])

values=  np.array([
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
])

print(values+rewards)

PT = genfromtxt('ptm_part1.csv', delimiter=',')
print(PT.shape)

MAX_ITERS = 150
tolerance = 0.001

for it in range(MAX_ITERS):
    print("iteration: ", it+1)
    values_new = np.matmul(PT, values) + rewards
    if np.allclose(values_new, values, atol=tolerance, rtol=0):
        break
    values = values_new

values = np.round(values, 3)
print(values)

# PART 2

import numpy as np
from numpy import genfromtxt


rewards = np.array([
    20, #A
    -1, #B
    -1, #C
    -1, #D
    -1, #E
    -1, #F
    2, #G
    -1, #H
    -1, #I
    2, #J
    -1, #K
    -1, #L
    -1, #M
    -1, #N
    -1, #P
    -20 #Q
])

values=  np.array([
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
])

print(values+rewards)

PT = genfromtxt('ptm5_part2.csv', delimiter=',')
print(PT.shape)

MAX_ITERS = 150
tolerance = 0.001
gamma = 0.9

for it in range(MAX_ITERS):
    print("iteration: ", it+1)
    values_new = rewards + gamma*np.matmul(PT, values)
    if np.allclose(values_new, values, atol=tolerance, rtol=0):
        break
    values = values_new

values = np.round(values, 3)
print(values.reshape(4, 4))
