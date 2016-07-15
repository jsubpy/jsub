#coding:utf-8
'''
Created on 2015-05-27 11:43:10

@author: suo
'''
import os,copy
from utility.Compress import tarDir

class Workflow(object):
    
    def __init__(self):
        self.jobSteps = []
        self.stepNumList = []
        self.jobParam = {}
        self.backend = None
    
    def setBackend(self,backend):
        self.backend = backend
            
    #---deepcopy?
    def setStepNumList(self,stepNumList):
        self.stepNumList = stepNumList
        
    def setJobSteps(self,jobSteps):
        self.jobSteps = jobSteps
        
    def setJobParam(self,jobParam):
        self.jobParam = jobParam
    #---
    
    def prepare(self,f):
        raise NotImplementedError

    def download(self,f):
        raise NotImplementedError
        
    def executeSteps(self,f):
        raise NotImplementedError
    
    def uploadData(self,f):
        raise NotImplementedError
        
    def complete(self,f):
        raise NotImplementedError
    
    def generateScript(self):
        try:
            with open(self.jobParam['jobScript'],'w') as f:
                self.prepare(f)
                self.download(f)
                self.executeSteps(f)
                self.uploadData(f)
                self.complete(f)
        except IOError as err:
            print 'IOError ',str(err)
        '''路径问题...'''
        rootDir =  os.path.dirname(os.getcwd())
        '''暂时把modules包下面的全部打包上传,待改'''         
        tarDir(os.path.join(rootDir,'jsub/modules/') ,os.path.join(self.jobParam['subDir'],'modules.tgz'))

    '''Independent of experiment and backend'''
    def scriptForDetermineQueue(self):
        if self.jobParam['totalJobs'] < 50 or self.jobPara['evtmax'] < 30:
            timeString = 'max_q_time = 0\n'
        elif self.jobParam['evtmax'] < 60:
            timeString = 'max_q_time = 60 * 5\n'
        elif self.jobParam['evtmax'] < 120:
            timeString = 'max_q_time = 60 * 10\n'
        else:
            timeString = 'max_q_time = 60 * 15\n'
        
        content = timeString+'''
if siteName.startswith('CLOUD'):
    max_q_time = 0
call(['python','determineQueue.py',str(max_q_time),jobID,'CEPC_script'])\n'''
            
        return content
            
if __name__ == '__main__':
    
    print os.getcwd()
    rootDir =  os.path.dirname(os.getcwd())#/home/suo/workspace2/jsub/jsub/
    print rootDir
    print os.path.join(rootDir,'modules/')#/home/suo/workspace2/jsub/jsub/modules/
#     tarDir(os.path.join(rootDir,'modules/') ,os.path.join('/home/suo/','modules.tgz'))        