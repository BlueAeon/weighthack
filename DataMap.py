#!/usr/bin/env python
from datetime import date, timedelta

# TODO:
## implement average() and plot()
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

    # TODO: Set unparsed variables as NoneType
    def parseFile(self, filestr):
        try:
            f = open(filestr)
        except FileNotFoundError:
            print("Cannot open file \"" + filestr + "\"")
            return 
        for line in f.read().splitlines():
            word = line.split(' ')
            self[word[0]].weight = word[1]
            self[word[0]].intake = word[2]
        f.close()
        return DataMap.pointcount 
         
    def __str__(self):
        ret = ""
        for key in self:
            ret += key + ": " + str(self[key].weight) + " " + str(self[key].intake) + "\n"
        return ret

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
    
    print(data['2015-03-16'].day)
    data.parseFile("sample_data")

    print(data)
    print(data['2015-03-02'].weight)
    print(data['2015-03-02'].intake)

if __name__ == "__main__":
    main()
