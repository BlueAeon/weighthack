#!/usr/bin/env python
from datetime import date, timedelta

# TODO:
## implement average() and plot()
class DataMap(dict):
    '''Base class is a perl-like autovivification object with built in vars
        for metrics that will be tracked. DataMap.day should be used for
        any date offset calculations. Right now dates MUST continue up until
        date.today()'''

    pointcount = 0              # total number of datapoints
    earliest = date.today()     # earliest date in data
    lbskcal = 3555              # calories per pound of fat

    def __init__(self, datestr=str(date.today()), weight=0, intake=0, avg=0, \
                    tdee=0):
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
        loopday = DataMap.earliest
        while loopday <= date.today():
            ret += str(loopday) + ": " + str(self[str(loopday)].weight) + \
                    " " + str(self[str(loopday)].intake) + " " + \
                    str(self[str(loopday)].avg) + " " + \
                    str(self[str(loopday)].tdee) + "\n"
            loopday += timedelta(days=1)
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
            self[word[0]].weight = float(word[1])
            self[word[0]].intake = int(word[2])
        f.close()
        return DataMap.pointcount 

    def avgWeight(self):
        loopday = DataMap.earliest
        while loopday < date.today():
            yavg = self[str(loopday - timedelta(days=1))].avg
            tlbs = self[str(loopday)].weight
            # calculate weight averages
            if yavg != 0 and tlbs != 0:
                self[str(loopday)].avg = round((tlbs + yavg)/2, 3)
            else:
                # restart average on missing data
                self[str(loopday)].avg = tlbs
            loopday += timedelta(days=1)

    def calcTDEE(self):
        '''Calculates the total energy supposedly used every day.'''
        loopday = DataMap.earliest
        while loopday <= date.today():
            ylbs = self[str(loopday - timedelta(days=1))].avg
            ycal = self[str(loopday - timedelta(days=1))].intake
            tlbs = self[str(loopday)].avg
            loopday += timedelta(days=1)
            if tlbs == 0 or ylbs == 0:
                continue
            tdee = int((ylbs - tlbs) * DataMap.lbskcal + ycal)
            self[str(loopday - timedelta(days=1))].tdee = tdee

    def avgTDEE(self):
        stub = ""

# for debugging
def main():
    data = DataMap()
    
    data.parseFile("sample_data")
    
    data.avgWeight()
    data.calcTDEE()
    print(data)
    print(data['2013-03-02'].weight)

    print(date(2015,3,1) - timedelta(days=1))
    print(data.earliest)

if __name__ == "__main__":
    main()
