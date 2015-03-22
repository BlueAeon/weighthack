#!/usr/bin/env python
from datetime import date, timedelta

# TODO:
## implement average() and plot()
class DataMap(dict):
    '''Base class is a perl-like autovivification object with built in vars
        for metrics that will be tracked. DataMap.day should be used for
        any date offset calculations'''

    pointcount = 0              # total number of datapoints
    earliest = date.today()     # earliest date in data

    def __init__(self, datestr=str(date.today()), weight=0, intake=0, avg=0, tdee=0):
        DataMap.pointcount += 1
        self.weight = weight
        self.intake = intake
        self.avg = avg
        self.tdee = tdee
        self.day = date(int(datestr.split('-')[0]),int(datestr.split('-')[1]), \
                            int(datestr.split('-')[2])) #clean this up somehow
        if self.day < DataMap.earliest:
            DataMap.earliest = self.day

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)(item)
            return value

    def __str__(self):
        ret = ""
        for key in self:
            ret += key + ": " + str(self[key].weight) + " " + \
                    str(self[key].intake) + " " + str(self[key].avg) + "\n"
        return ret

    # TODO: Set unparsed variables as NoneType
    def parseFile(self, filestr):
        ''' parseFile() expects a string whos path has a file which cointains
            newline sperated entries in the form "<date> <weight> <intake>\n"
            EG: 2015-03-14 194.2 1695 '''
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

    # figure out what to do with dates that are missing some data
    # since dictionaries are unsorted we need a way to iterate through every
    # date, calculating the average while skipping missing dates? OR
    # we could create every date before running the average and then find
    # the earliest and start there.
    def average(self, smooth):
        for key in self:
            stub = ""
            

# for debugging
def main():
    data = DataMap()
    
    data.parseFile("sample_data")
    
    data['2015-03-01'].weight = 160
    data['2015-03-01'].intake = 1500

    print(data)
    print(data['2015-03-02'].weight)

    print(date(2015,3,1) - timedelta(days=1))
    print(data.earliest)

if __name__ == "__main__":
    main()
