'''
Created on 2016-01-13 22:12:22

@author: suo
'''
from core.Workflow import Workflow

class JunoWorkflow(Workflow):
    def __init__(self):
        super(JunoWorkflow,self).__init__()
        
    def prepare(self, f):
        content = '''#!/usr/bin/env python
import sys
from subprocess import call
call(['hostname'])
call(['date'])
call(['ls','-l'])
call(['echo','set','env'])
call(['ls','/cvmfs/juno.ihep.ac.cn/'])
call(['source','/cvmfs/juno.ihep.ac.cn/sl6_amd64_gcc44/J14v1r1/setup.sh'])
'''
        f.write(content)
    
    def download(self,f):
        pass
    
    def executeSteps(self, f):
        if '1' in self.stepNumList:
            sim = self.jobSteps[self.stepNumList.index('1')]
            args = '''--seed %s --evtmax %s --output sample_detsim_%s.root --user-output sample_detsim_user_%s.root'''%\
            (self.jobParam['seed'],self.jobParam['eventNum'],self.jobParam['index'],self.jobParam['index'])           
            if hasattr(sim, 'args'):
                args+=sim.args           
            content = '''\n\'''********************Execute Simulation********************\'''
print 'start simu job'
# python %s %s &> juno-sim.log
sim_result = call(['python','%s','%s','&>','juno-sim.log'])
if sim_result!=0:
    sys.exit(1)
''' % ('tut_detsim.py',args)
            f.write(content)
            
        if '2.1' in self.stepNumList:
            calib = self.jobSteps[self.stepNumList.index('2.1')]
            args = '''--seed %s --input sample_detsim_%s.root --output sample_calib_%s.root'''%\
            (self.jobParam['seed'],self.jobParam['index'],self.jobParam['index'])
            if hasattr(calib, 'args'):
                args+=calib.args
            content = '''\n\'''********************Execute Caliberation&Reconstruction********************\'''
print 'start rec job'
rec1_result = call(['python','%s','%s','&>','juno-rec1.log'])
if rec1_result!=0:
    sys.exit(1)
''' % ('tut_det2calib.py',args)
            f.write(content)
            
        if '2.2' in self.stepNumList:
            rec = self.jobSteps[self.stepNumList.index('2.2')]
            args = '''--seed %s --input sample_calib_%s.root --output sample_rec_%s.root'''%\
            (self.jobParam['seed'],self.jobParam['index'],self.jobParam['index'])
            if hasattr(rec, 'args'):
                args+=rec.args
            content = '''
rec2_result = call(['python','%s','%s','$>','juno-rec2.log'])
if rec2_result!=0:
    sys.exit(1)
''' %('tut_calib2rec.py',args)
            f.write(content)
    
    def uploadData(self,f):
        pass
    
    def complete(self, f):
        content = '''\n\'''********************Job Completed********************\'''
call(['ls','-l'])
call(['mv','geometry_acrylic.gdml geometry_acrylic_%s.gdml'])
call(['ls','-l'])
call(['date'])
print 'All Done'
'''%self.jobParam['index']
        f.write(content)