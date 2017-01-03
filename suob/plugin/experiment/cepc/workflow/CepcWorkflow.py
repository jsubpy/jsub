'''
Created on 2015-06-24 11:03:54

@author: suo
'''
from core.Workflow import Workflow

class CepcWorkflow(Workflow):
    
    def __init__(self):
        super(CepcWorkflow,self).__init__()
    
    def prepare(self, f):
        content = '''#!/usr/bin/env python
import sys,os,tarfile
from subprocess import call
'''+\
        self.backend.scriptForImport()+\
        self.backend.scriptForJobID()+\
'''
call(['python','setJobStatus.py',jobID,'CEPC_script','Preparation'])    #---------RELATIED TO BACKEND---------

tarobj = tarfile.open('modules.tgz', "r:gz")
tarobj.extractall()
tarobj.close()

call(['python','checkExeEnv.py'])

result = call(['python','checkCvmfs.py','/cvmfs/cepc.ihep.ac.cn/'])    
if result!=0:
    call(['python','setJobStatus.py',jobID,'CEPC_script','cvmfs not found']) #---------RELATIED TO BACKEND---------
    sys.exit(result)

call(['python','tmsg.py','Files from inputSandbox:'])
call(['ls','-l'])

siteName = ''
'''
        if hasattr(self.backend, 'scriptForSiteName'):
            content +=self.backend.scriptForSiteName()
        if hasattr(self.backend, 'scriptForDetermineMirrorDB'):
            content +=self.backend.scriptForDetermineMirrorDB()
        
        content+=self.scriptForDetermineQueue()
        
        f.write(content)

    def download(self,f):
        pass
    
    def executeSteps(self, f):
        if '1' in self.stepNumList:
            sim = self.jobSteps[self.stepNumList.index('1')]
            content = '''\n\'''********************Execute Simulation********************\'''
call(['python','tmsg.py','Generate shell script for simulation'])
call(['chmod','755','simu.sh'])
call(['python','setJobStatus.py',jobID,'CEPC_script','%s Simulation'])    #---------RELATIED TO BACKEND---------
call(['python','tmsg.py','Start simulation'])
simu_result = call(['./simu.sh','%s'])

check_sim_result = call(['python','checkSimuLog.py',str(simu_result)])
if check_sim_result == 21:
    call(['python','setJobStatus.py',jobID,'CEPC_Script','DB connection failed'])
elif check_sim_result == 20:
    call(['python','setJobStatus.py',jobID,'CEPC_Script','Simulation Error'])\n''' % (sim.executable,sim.executable) #---------RELATIED TO BACKEND---------
            f.write(content)
            
        if '2' in self.stepNumList:
            rec = self.jobSteps[self.stepNumList.index('2')]
            content = '''\n\'''********************Execute Reconstruction********************\'''
call(['python','tmsg.py','Generate shell script for reconstruction'])
call(['chmod','755','reco.sh'])
call(['python','setJobStatus.py',jobID,'CEPC_script','%s Reconstruction'])    #---------RELATIED TO BACKEND---------
call(['python','tmsg.py','Start reconstruction'])
call(['./reco.sh','%s'])

check_reco_result = call(['python','checkRecoLog.py','%s'])
if check_reco_result == 30:
    call(['python','setJobStatus.py',jobID,'CEPC_script','Reconstruction Error'])\n''' % (rec.executable,rec.executable,self.jobParam['eventNum'])  #---------RELATIED TO BACKEND---------
            f.write(content)
        
    def uploadData(self,f): 
    #---------RELATIED TO BACKEND---------
        if hasattr(self.backend, 'scriptForUploadData'):
            content = self.backend.scriptForUploadData(self.jobParam)   
        f.write(content)        
    
    def complete(self,f):
        content ='''\n\'''********************Job Completed********************\'''
call(['python','tmsg.py','Job Completed. Files in current dir:'])
call(['ls','-l'])
call(['python','setJobStatus.py',jobID,'CEPC_script','Done'])    #---------RELATIED TO BACKEND---------
call(['python','tmsg.py','Job Done'])\n'''
        f.write(content)
                     
if __name__ == '__main__':
    import os
    w  = CepcWorkflow()
    w.stepNumList = ['1','2']
    w.jobPara = {'totalJobs':50,'evtmax':30}
    w.scriptpath = os.path.join(os.getcwd(),'maintest.py')
    w.generateScript()