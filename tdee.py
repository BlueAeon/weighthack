#!/usr/bin/env python
import sys

sys.setrecursionlimit(10000)    
maxdepth = 50 # max depth for recursive functions                              

if len(sys.argv) < 2:
    sys.exit('Usage: ./tdee.py <days> <logfile>')

# the average of a given day Asub(d) 
# the measurement of a day Msub(d)
# The smoothing constant S (eg: .9) 
# The smoothing Percentage P (1 - S) 
# Asub(d) = Asub(d-1) + P * (Msub(d) - Asub(d-1))

# Curved moving averages
## term: Array of values to average
## depth: Maximum depth to recurse
def avg(term, depth):
    print(term[depth-1], depth)
    if depth > 0:
        avg(term, depth-1)

weights = [190,190,180,190,185,180,185]
ndays = 7

if ndays > maxdepth:
    ndays = maxdepth
avg(weights,7)
