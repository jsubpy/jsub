'''
Created on 2016-01-12 16:32:48

@author: suo
'''
from core.Step import Step

class Sim(Step):
    def __init__(self,stepDict = None, name=None):
        super(Sim,self).__init__(stepDict)
        self.number = '1'
        if name!=None:
            self.description = 'This is Juno Sim: '+name
            
class Calib(Step):
    def __init__(self,stepDict = None, name=None):
        super(Sim,self).__init__(stepDict)
        self.number = '2.1'
        if name!=None:
            self.description = 'This is Juno Calib: '+name
            
class Rec(Step):
    def __init__(self,stepDict = None, name=None):
        super(Sim,self).__init__(stepDict)
        self.number = '2.2'
        if name!=None:
            self.description = 'This is Juno Rec: '+name