#coding:utf-8
'''
Created on 2015-12-16 03:20:55

@author: suo
'''
import os
from subprocess import call
from core.Backend import Backend

class Condor(Backend):
    def __init__(self, backendDict = None):
        if backendDict:
            self.outputDir = backendDict['OutputDir']
        else:
            self.outputDir = ''
    
    def submit(self, jobSet):
        '''创建submit description file'''
        if len(jobSet)!=0 and jobSet[0]['masterDir']:
            submitDescription = os.path.join(jobSet[0]['masterDir'],'submit')
            
        '''如果以w方式打开，即使文件不存在也会创建，而不会抛出异常'''            
        with open(submitDescription,'w') as f:
            content = '''Universe       = vanilla
Executable     = $(SubDir)/runtimeScript.py
Log            = job.log
Output         = job.out
Error          = job.err

should_transfer_files = YES
when_to_transfer_output = ON_EXIT_OR_EVICT
'''
            f.write(content)
            
            if not os.path.isdir(self.outputDir):
                print self.outputDir
                os.mkdir(self.outputDir)
                
            count =1                
            for jobParam in jobSet:
                outputSubDir = os.path.join(self.outputDir,str(count))
                os.mkdir(outputSubDir)
                content='''
transfer_input_files = %s, $(MasterDir)/, $(SubDir)/
MasterDir            = %s
SubDir               = %s
InitialDir           = %s
Queue
'''%(jobParam['inputFilePath'],
     jobParam['masterDir'],
     jobParam['subDir'],
     outputSubDir
     )
     
                f.write(content)
                count+=1
        #call(['condor_submit',submitDescription])

    def getInputFilePrefix(self,experiment):
        return ''
    
    def getOutputDataPath(self,experiment,*args):
        path = self.outputDir
        for each in args:
            path = os.path.join(path,each)
        return path
    
    def registerInputData(self, filepath,size, experiment):
        pass
    
    '''----------------------------------------------------------------------------'''
    '''----------------------------------------------------------------------------'''
    def scriptForImport(self):
        return ''
    
    def scriptForJobID(self):
        return ''
    
if __name__ == '__main__':
    backend = Condor()
#     jobSet = [
#               {'masterDir':'/home/suo/','subDir':'/home/suo/1','totalJobs':3,'inputFilePath':'/home/suo/Pze1'},
#               {'masterDir':'/home/suo/','subDir':'/home/suo/2','totalJobs':3,'inputFilePath':'/home/suo/Pze2'},
#               {'masterDir':'/home/suo/','subDir':'/home/suo/3','totalJobs':3,'inputFilePath':'/home/suo/Pze3'},
#              ]
#     backend.submit(jobSet)
