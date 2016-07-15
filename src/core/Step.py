'''
Created on 2015-06-01 11:19:23

@author: suo
'''

class Step(object):
    def __init__(self, stepDict= None):
        if stepDict!=None:
            self.executable = stepDict['Executable']
            if 'JobOption' in stepDict and type(stepDict['JobOption']) == type([]):
                self.jobOption = stepDict['JobOption']
            elif 'JobOption' in stepDict and type(stepDict['JobOption']) == type(""):
                self.jobOption = [stepDict['JobOption']]
                
            if 'Args' in stepDict:
                self.args = stepDict['Args']
                
            self.returnData = stepDict['ReturnData']
        else:
#             self.executable = ''
#             self.jobOption = []
            self.returnData = False
            
        self.description = 'This is the abstract step'
#         self.optionsParser = None
        self.modules = []
        self.number = None
        
    def setJobOption(self, value):
        pass
    
#     def resolveOptions(self):
#         self.optionsParser.parse()