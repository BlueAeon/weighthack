#!/usr/bin/env python
from datetime import date, timedelta

# TODO:
## implement average() and plot(), implement gnuplot or scipy
## fix the weight curve
class DataMap(dict):
    '''Base class is a perl-like autovivification object with built in vars
        for metrics that will be tracked. DataMap.day should be used for
        any date offset calculations. Right now dates MUST continue up until
        date.today()'''

    pointcount = 0              # total number of datapoints
    earliest = date.today()     # earliest date in data
    lbskcal = 3555              # calories per pound of fat
    tperiod = 14                 # days to average TDEE over

    def __init__(self, datestr=str(date.today()), weight=-1, intake=-1, wavg=-1, \
                    tdee=-1, tavg=-1):
        DataMap.pointcount += 1
        self.weight = weight
        self.intake = intake
        self.tavg = tavg
        self.wavg = wavg
        self.tdee = tdee
        year = int(datestr.split('-')[0])
        month = int(datestr.split('-')[1])
        day = int(datestr.split('-')[2])
        self.day = date(year, month, day)
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
            datestr = str(self[str(loopday)].day)
            lbs = str(self[str(loopday)].weight)
            intake = str(self[str(loopday)].intake)
            avgw = str(self[str(loopday)].wavg)
            tdee = str(self[str(loopday)].tdee)
            tavg = str(self[str(loopday)].tavg)
            if "-1" in (lbs, intake, avgw, tdee, tavg): # remove with gnuplot
                ret += "\n"
            else:
                ret += datestr + " " + lbs + " " + avgw + " " + intake + " " + \
                    tdee + " " + tavg + "\n"
            loopday += timedelta(days=1)
        return ret

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
            # What to do when there's missing data? Skip to next and let 
            # GNUPlot average? Set to zero and ruin our averages?
            if len(word) < 2:
                continue
            try:
                self[word[0]].weight = float(word[1])
            except (IndexError, ValueError) as e:
                self[word[0]].weight = -1 
                continue
            try:
                self[word[0]].intake = int(word[2])
            except (IndexError, ValueError) as e:
                self[word[0]].intake = -1 
                continue
        f.close()
        return DataMap.pointcount 

    def avgWeight(self):
        loopday = DataMap.earliest
        while loopday < date.today():
            yavg = self[str(loopday - timedelta(days=1))].wavg
            tlbs = self[str(loopday)].weight
            # calculate weight averages
            if yavg != 0 and tlbs != 0:
                self[str(loopday)].wavg = round((tlbs + yavg)/2, 3)
            else:
                # restart average on missing data
                self[str(loopday)].wavg = tlbs
            loopday += timedelta(days=1)

    def calcTDEE(self):
        '''Calculates the total energy supposedly used every day.'''
        loopday = DataMap.earliest
        while loopday <= date.today():
            ylbs = self[str(loopday - timedelta(days=DataMap.tperiod))].wavg
            tlbs = self[str(loopday)].wavg
            if ylbs == -1: # handle first tperiod of data
                ylbs = tlbs
            totallbs = ylbs - tlbs
            totalcal = totallbs * DataMap.lbskcal
            i = 0
            while i < DataMap.tperiod:
                cal = self[str(loopday - timedelta(days=i))].intake
                if cal == -1:
                    break 
                totalcal += cal
                i += 1
            loopday += timedelta(days=1)
            if tlbs == -1 or ylbs == -1 or i == 0:
                continue
            tdee = int(totalcal / i)
            self[str(loopday - timedelta(days=1))].tdee = tdee

    def avgTDEE(self):
        loopday = DataMap.earliest
        while loopday <= date.today():
            yavg = self[str(loopday - timedelta(days=1))].tavg
            ttdee = self[str(loopday)].tdee
            if yavg != 0 and ttdee != 0:
                self[str(loopday)].tavg = int((yavg + ttdee)/2)
            else:
                # reset average if day is missing?
                self[str(loopday)].tavg = ttdee
            loopday += timedelta(days=1)

# for debugging
def main():
    data = DataMap()
    data.parseFile("sample_data")
    data.avgWeight()
    data.calcTDEE()
    data.avgTDEE()
    
    # need to figure out how to clean up empty dicts
    # Maybe start at earlist and loop forward checking for 
    # Unset DataMaps (hackish)
    # del data['2015-03-20']

    print(data)
   
if __name__ == "__main__":
    main()
