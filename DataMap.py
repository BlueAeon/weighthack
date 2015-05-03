#!/usr/bin/env python
from datetime import date, timedelta
import numpy as np

class DataMap(dict):
    '''Base class is a perl-like autovivification object with built in vars
        for metrics that will be tracked. DataMap.day should be used for
        any date offset calculations. Right now dates MUST continue up until
        date.today()'''

    pointcount = 0              # total number of datapoints
    earliest = date.today()     # earliest date in data
    lbskcal = 3555              # calories per pound of fat
    tperiod = 14                # days to average TDEE over
    wsize = 20                  # EMA window size
    guesswin = 3                # EMA window size for guessing

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
        loopday = self.earliest
        while loopday <= date.today():
            datestr = str(self[str(loopday)].day)
            lbs = str(self[str(loopday)].weight)
            intake = str(self[str(loopday)].intake)
            avgw = str(self[str(loopday)].wavg)
            tdee = str(self[str(loopday)].tdee)
            tavg = str(self[str(loopday)].tavg)
            if "-1" in (lbs, intake, avgw, tdee, tavg): # remove with gnuplot
                ret += "REJECTED:"
                ret += datestr + " " + lbs + " " + avgw + " " + intake + " " + \
                    tdee + " " + tavg + "\n"
                #ret += "\n"
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

    def EMA(self, values, window):
        weights = np.exp(np.linspace(-1., 0., window))
        weights /= weights.sum()
        a = np.convolve(values, weights)[:len(values)]
        a[:window] = a[window]
        return a

    def avgWeight(self, startdate):
        ''' Generate exponentially curved moving average of weight'''
        lbs = []
        loopday = startdate

        while loopday < date.today():
            lbs.append(self[str(loopday)].weight)
            loopday += timedelta(days=1)

        # First pass average
        albs = self.EMA(lbs, self.wsize)

        # Fix starting point
        albs[0] = self[str(startdate)].weight

        # Fix early dates
        for index in range(1, self.wsize):
            # This is really inefficient
            # from zero to wsize call EMA, save last result to albs 
            temp = self.EMA(lbs, index)
            albs[index] = temp[index]
            #print(temp)
            
        loopday = startdate
        for i in range(0, albs.size):
            self[str(loopday + timedelta(days=i))].wavg = round(albs[i],1)

    def avgTDEE(self, startdate):
        tdee = []
        loopday = DataMap.earliest

        while loopday <= date.today():
            tdee.append(self[str(loopday)].tdee)
            loopday += timedelta(days=1)

        atdee = self.EMA(tdee, self.wsize)
        atdee[0] = self[str(startdate)].tdee
        for index in range(1, self.wsize):
            temp = self.EMA(tdee, index)
            atdee[index] = temp[index]
        loopday = startdate
        for i in range(0, atdee.size):
            self[str(loopday + timedelta(days=1))].tavg = round(atdee[i],1)

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


    # guessIntake will read back wsize (e.g: 20) days, recalculate weight with a n-day 
    # average then guess intake on the assumption that TDEE has stayed the same.
    # Eventually seperate out plots for real/guessed values
    def guessIntake(self, date):
        # Find difference from yesterdays weight with n-day EMA
        lbs = []
        albs = []
        date -= timedelta(days=self.wsize)
        # Create weight average array
        for i in range(0, self.wsize):
            x = self[str(date + timedelta(days=i))].wavg
            if x == -1:             #update this to work before n days?
                return
            lbs.append(x)
        date += timedelta(days=self.wsize)
        albs = self.EMA(lbs, self.guesswin)
        # difference from yesterday (use n-day avg for better accuracy)
        diff = albs[self.wsize-1] - albs[self.wsize-2]
        tdee = self[str(date - timedelta(days=1))].tdee
        self[str(date)].tdee = tdee                 # Carry over yesterdays TDEE
        intake = int(tdee + (diff * self.lbskcal))
        self[str(date)].intake = intake

    def guessWeight(self, startdate):
        ''' Iterates through weights and plots a straight line between missing days '''
        loopday = startdate
        if self[str(loopday - timedelta(days=1))].weight == -1:    # fail without weight history
            return
        while self[str(loopday)].weight == -1:
            loopday += timedelta(days=1)

        # calc difference per day
        time = (loopday - startdate).days
        distance = self[str(loopday)].weight - self[str(startdate - timedelta(days=1))].weight 
        rate = distance / time
        #print("loopday.weight: " + str(self[str(loopday)].weight))
        #print("startdate.weight: " + str(self[str(startdate - timedelta(days=1))].weight))
        #print("Date: " + str(startdate) + " Rate: " + str(rate) + " Distance: " + str(distance) + " Time: " + str(time))

        # loop through setting weight
        while startdate < loopday:
            self[str(startdate)].weight = round(self[str(startdate - timedelta(days=1))].weight + rate, 1)
            #print("Guessing weight: " + str(self[str(startdate)].weight))
            startdate += timedelta(days=1)
    
    def guessMissingData(self):
        loopday = DataMap.earliest
        while loopday < date.today():
            if self[str(loopday)].intake == -1:
                self.guessIntake(loopday)
            if self[str(loopday)].weight == -1:
                self.guessWeight(loopday)
            loopday += timedelta(days=1)

    def findEarliest(self):
        # TODO: Figure out how to add this into DataMap constructors
        ''' Correctly sets earliest to date with intake or weight. '''
        while self.earliest < date.today():
            if self[str(self.earliest)].weight != -1:
                return
            if self[str(self.earliest)].intake != -1:
                return
            self.earliest += timedelta(days=1)

# for debugging
def main():
    data = DataMap()
    data.parseFile("sample_data")
    data.findEarliest()
    data.avgWeight(data.earliest)
    data.calcTDEE()
    data.guessMissingData()
    data.avgTDEE(data.earliest)
    
    # need to figure out how to clean up empty dicts
    # Maybe start at earlist and loop forward checking for 
    # Unset DataMaps (hackish)
    # del data['2015-03-20']

    print(data)
    #print(data.earliest)
   
if __name__ == "__main__":
    main()
