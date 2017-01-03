'''
Created on 2015-06-09 20:24:22

@author: suo
'''
from core.splitter.Splitter import Splitter

class SplitterByEvent(Splitter):
    def __init__(self,eventPer = None,eventTotal = None, seedStart = None, splitterDict = None):
        print 'This is SplitterByEvent __init__()'
        if splitterDict:
            self.eventMaxPerJob = splitterDict['EventMaxPerJob']
            self.eventTotal = eval(splitterDict['EventTotal'])
            if splitterDict['SeedStart'] == 'auto':
                self.seedStart = self.getSeedStart()
        else:
            self.eventMaxPerJob = ''
            self.eventTotal = ''
            self.seedStart = ''
        if eventPer:
            self.eventMaxPerJob = eventPer
        if eventTotal:
            self.eventTotal = eventTotal
        if seedStart:
            self.seedStart = seedStart
        else:
            self.seedStart = self.getSeedStart()
            
    def getSeedStart(self):
        return 1
    
    def split(self):
        eventList = self._split(self.eventMaxPerJob, self.eventTotal)
        seed = self.seedStart
        result = []
        index = 1
        for event in eventList:
            aDict = {'index':str(index),
                     'seed':str(seed), 
                     'eventNum':event}
            result.append(aDict)
            seed+=1
            index+=1
        return result
    
    def _split(self,per,total):
        evtList = []
        num = -(-total//per)
        for i in range(1,num+1):
            if i<num:
                evtList.append(per)
            else:
                evtList.append(total-per*(num-1))
        return evtList