#coding:utf-8
'''
Created on 2015-07-03 14:40:28

@author: suo
'''
import os,copy
from utility.Workspace import createMasterRepoDir
from utility.UserConf import repo_path

class JobFactory(object):
    
    def __init__(self):
        self.properties = {'inputSandbox':{},'outputSandbox':{}}
    
    def createJobSet(self,experiment,splitter,backend,stepNumList):
        masterDir = createMasterRepoDir(repo_path)
        count = 1
        subjobs = []
        jobParam = {'experiment':experiment,
                    'jobScriptLog':'script.log',
                    'inputSandbox':[],
                    'outputSandbox':['script.log','job.log','job.err'],#in Condor: job.out, job.log, job.error
                    'outputData':[],
                    'masterDir': masterDir}
        #outputsandbox可以统一处理
        if '1' in stepNumList:
            jobParam['outputSandbox'].extend(self.properties['outputSandbox']['sim'])
        if '2.1' in stepNumList:
            jobParam['outputSandbox'].extend(self.properties['outputSandbox']['calib'])
        if '2.2' in stepNumList or '2' in stepNumList:
            jobParam['outputSandbox'].extend(self.properties['outputSandbox']['rec'])
#         if '3' in stepNumList:
#             jobParam['outputSandbox'].extend(self.properties['outputSandbox']['ana'])

        splitResult = splitter.split() 
        jobParam['totalJobs'] = len(splitResult)
     
        for eachDict in splitResult:
            currentjobParam = copy.deepcopy(jobParam)
#             for key in eachDict:
#                 currentjobParam[key] = eachDict[key]
            '''把每个split的作业参数都加进来'''
            currentjobParam.update(eachDict)
            
            '''为每个subjob赋值'''            
            self.setSubParam(currentjobParam, count)
            self.setSpecialParam(currentjobParam, backend, stepNumList)
            
            subjobs.append(currentjobParam)
            count+=1

        return subjobs
    
    def setSubParam(self,jobParam,count):
        '''主要是subDir不一样;对于不同实验,处理方式一样'''
        jobParam['subDir'] = os.path.join(jobParam['masterDir'],str(count))
        os.mkdir(jobParam['subDir'])
        jobParam['jobName'] = "%s_v1_%s_%s"%(jobParam['experiment'],os.path.basename(jobParam['masterDir']),str(count))
        jobParam['jobScript'] = os.path.join(jobParam['subDir'],'runtimeScript.py')
        jobParam['inputSandbox'].append(jobParam['jobScript'])
        
        jobParam['inputSandbox'].append(os.path.join(jobParam['subDir'],'modules.tgz'))
                
    def setSpecialParam(self,jobParam,backend,stepNumList):
        '''每个实验特有的处理方式,必须重写'''
        raise NotImplementedError           