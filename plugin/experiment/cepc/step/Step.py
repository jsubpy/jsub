#!coding:utf-8
'''
Created on 2015-06-01 12:54:09

@author: suo
'''
from core.Step import Step
from experiment.cepc.optsparser.CepcSimParser import CepcSimParser
from experiment.cepc.optsparser.CepcRecParser import CepcRecParser 

'''CEPC Steps'''
class Sim(Step):
    def __init__(self,stepDict = None,name=None):
        super(Sim, self).__init__(stepDict)
        if 'MirrorDB' in stepDict and stepDict['MirrorDB']:
            self.mirrorDB = stepDict['MirrorDB']
        else:#需不需要强制指定...
            self.mirrorDB = ''     
        self.number = '1'
        self.optionsParser = CepcSimParser(self.jobOption,self.mirrorDB)
        if name!=None:
            self.description = 'This is Cepc Sim: '+name

class Rec(Step):
    def __init__(self,stepDict = None,name=None):
        super(Rec, self).__init__(stepDict)
        self.number = '2'
        self.optionsParser = CepcRecParser(self.jobOption)
        if name!=None:  
            self.description = 'This is Cepc Rec: '+name

if __name__ == '__main__':
    s = Sim(name='Mokka')