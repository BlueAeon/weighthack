#!/usr/bin/env python
from datetime import date, timedelta

# TODO:
## implement average() and parseFile() and plot()
class DataMap(dict):
    '''Base class is a perl-like autovivification object with built in vars
        for metrics that will be tracked. DataMap.day should be used for
        any date offset calculations'''
    pointcount = 0 
    def __init__(self, datestr="1987-11-02", weight=0, intake=0, avg=0, tdee=0):
        DataMap.pointcount += 1
        self.weight = weight
        self.intake = intake
        self.day = date(int(datestr.split('-')[0]),int(datestr.split('-')[1]), \
                            int(datestr.split('-')[2])) #clean this up somehow
        self.avg = avg
        self.tdee = tdee
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)(item)
            return value

# Just for debugging
def main():
    data = DataMap()
    data['2015-03-20'].weight = 190
    data['2015-03-20'].intake = 1000
    data['2015-03-18'].weight = 195
    data['2015-03-18'].intake = 1002
    data['2015-03-17'].weight = 200
    data['2015-03-17'].intake = 1003
    data['2015-03-16'].weight = 180
    data['2015-03-16'].intake = 1004
    
    print(data)
    for key in data:
        print(data[key].weight)

    print(data['2015-03-16'].day)

if __name__ == "__main__":
    main()
