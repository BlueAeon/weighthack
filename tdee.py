#!/usr/bin/env python
import sys
import datetime

# Shamelessly ripped from stackoverflow.com
class Vivify(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def avg(input, smooth):
    for i in range(len(input)):
        if i == 0:
            result[i] = input[i]
        else:
            result.append(result[i-1] + (1 - smooth)*(input[i] - result[i-1]))

def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: ./tdee.py <logfile>')
    # for a date format we're just going to use days since epoch
    epoch = datetime.datetime.utcfromtimestamp(0)
    print(epoch.days())
    data = Vivify()
    f = open(sys.argv[1],'r')
    for line in f.read().splitlines():
        word = line.split(' ')
        data[word[0]]['weight'] = word[1] 
        data[word[0]]['intake'] = word[2] 
    print(data)
    # take all the weights and put them into an array
    # calculate average
    # put the averages into matching dates
    print(len(data))
    weight = [190,190,180,190,185,180,185]
    average = [None]
    smooth = .9
    avg(weight, average, smooth) 

if __name__ == "__main__":
    main()
