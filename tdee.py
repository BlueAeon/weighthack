#!/usr/bin/env python
import sys

sys.setrecursionlimit(10000)    
max = 50 # max depth for recursive functions                              

if len(sys.argv) < 2:
    sys.exit('Usage: ./tdee.py <days> <logfile>')

# the average of a given day Asub(d) 
# the measurement of a day Msub(d)
# The smoothing constant S (eg: .9) 
# The smoothing Percentage P (1 - S) 
# Asub(d) = Asub(d-1) + P * (Msub(d) - Asub(d-1))

# Curved moving averages
# prepare for brain-assault
## term: Array of values to average
## depth: Maximum depth to recurse
## smooth: Smoothing constant
## maxdepth: Maximum depth to step backwards into list
# average = smooth * average + (1 - smooth) * term
def avg(term, depth, smooth, maxdepth):
    average = term[depth]
    print(term[depth],depth,len(term)-depth,maxdepth)
    if depth > 0 and len(term)-depth < maxdepth: 
        # at [1] this returns M[0]
        average = avg(term, depth-1, smooth, maxdepth)
    return average

weights = [190,190,180,190,185,180,185]
ndays = len(weights) - 1
if ndays > max:
    ndays = max
#avg(weights, ndays, .9, max) 

average = weights[0]
smooth = .9
for weight in weights:
    average = 
    print(average)

# start with an empty array of averages the same length of weights
# set average[0] to weight[0]
# average[i] = average[i-1] + (1 - smooth)*(weight[i] - average[i-1)
