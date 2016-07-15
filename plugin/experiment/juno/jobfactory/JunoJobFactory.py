'''
Created on 2016-01-13 21:45:09

@author: suo
'''
from core.JobFactory import JobFactory

class JunoJobFactory(JobFactory):
    
    def __init__(self):
        super(JunoJobFactory, self).__init__()
        self.properties['inputSandbox']['sim'] = []
        self.properties['inputSandbox']['calib'] = []
        self.properties['inputSandbox']['rec'] = []
        
        self.properties['outputSandbox']['sim'] = ['juno-sim.log']
        self.properties['outputSandbox']['calib'] = ['juno-rec1.log']
        self.properties['outputSandbox']['rec'] = ['juno-rec2.log']
        
    def setSpecialParam(self, jobParam, backend, stepNumList):
        if '1' in stepNumList:
            jobParam['outputData'].append(backend.getOutputDataPath(experiment = 'juno','sim','sample_detsim_%s.root'%jobParam['index']))
            jobParam['outputData'].append(backend.getOutputDataPath(experiment = 'juno','sim','sample_detsim_user_%s.root'%jobParam['index']))        
        if '2.1' in stepNumList:
            jobParam['outputData'].append(backend.getOutputDataPath(experiment = 'juno','rec','sample_calib_%s.root'%jobParam['index']))
        if '2.2' in stepNumList or '2' in stepNumList:    
            jobParam['outputData'].append(backend.getOutputDataPath(experiment = 'juno','rec','sample_rec_%s.root'%jobParam['index']))
            jobParam['outputData'].append(backend.getOutputDataPath(experiment = 'juno','rec','geometry_acrylic_%s.gdml'%jobParam['index']))