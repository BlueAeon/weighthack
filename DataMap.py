#!/usr/bin/env python
# stuff I'm looking for
# object['date'].weight = 10000
# object['date'].intake = 10000
# object.average()
# object.parseFile(sample_data)

# TODO:
## implement average() and parseFile()
## track date as an integer friendly datetime object
### EG: data[date-1].weight = blah
class DataMap(dict):
    '''Base class is a perl-like autovivification object with built in vars
        for metrics that will be tracked'''
    pointcount = 0 
    def __init__(self,date="", weight=0, intake=0, avg=0):
        DataMap.pointcount += 1
        self.weight = weight
        self.intake = intake
        self.date = date
        self.avg = avg
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
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

if __name__ == "__main__":
    main()
