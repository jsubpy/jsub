#coding:utf-8
'''
Created on 2015-07-06 15:42:47

@author: suo
'''
import os
from core.JobFactory import JobFactory

class CepcJobFactory(JobFactory):
    
    def __init__(self):
        super(CepcJobFactory, self).__init__()
        self.properties['inputSandbox']['sim'] = ['simu.macro','event.macro']
        self.properties['inputSandbox']['rec'] = ['PandoraSettingsDefault.xml','PandoraLikelihoodData9EBin.xml','reco.xml']
        
        self.properties['outputSandbox']['sim'] = ['simu.macro','simu.sh','simu.log']
        self.properties['outputSandbox']['rec'] = ['reco.sh','reco.log']
                
    def setSpecialParam(self, jobParam, backend, stepNumList):
        if hasattr(backend, 'outputSE'):                
            jobParam['se'] = backend.outputSE
        
        if 'inputFilePath' in jobParam:
            #stdhep文件加到inputsandbox里,dirac会下载
            jobParam['inputSandbox'].append(backend.getInputFilePrefix('cepc')+jobParam['inputFilePath'])

        if '1' in stepNumList:
            jobParam['inputSandbox'].extend([os.path.join(jobParam['subDir'],each) for each in self.properties['inputSandbox']['sim']])
            
            jobParam['outputData'].append(backend.getOutputDataPath(experiment= 'cepc','sim',os.path.splitext(jobParam['inputFileName'])[0]+'_sim.slcio'))
            
        if '2' in stepNumList:
            ''''PandoraSettingsDefault.xml','PandoraLikelihoodData9EBin.xml仅在master下'''
            jobParam['inputSandbox'].extend([os.path.join(jobParam['masterDir'],each) for each in ['PandoraSettingsDefault.xml','PandoraLikelihoodData9EBin.xml']])
            jobParam['inputSandbox'].append(os.path.join(jobParam['subDir'],'reco.xml'))
            
            jobParam['outputData'].append(backend.getOutputDataPath(experiment= 'cepc','rec',os.path.splitext(jobParam['inputFileName'])[0]+'_rec.slcio'))
