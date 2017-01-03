'''
Created on 2015-06-30 22:26:30

@author: suo
'''
import os,commands
from utility.ResolvePath import trimJoinPathElement
from core.Backend import Backend
from DIRAC.Interfaces.API.Dirac import Dirac as GridDirac
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Core.Security.ProxyInfo import getProxyInfo
from DIRAC.Core.Base import Script
from modules.setJobStatus import experiment
Script.parseCommandLine( ignoreErrors = False )
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC.DataManagementSystem.Client.ReplicaManager import ReplicaManager

class Dirac(Backend):
    def __init__(self, backendDict = None):
        if backendDict:
            self.site = backendDict['Site']
            self.jobGroup = backendDict['JobGroup']
            self.outputSE = backendDict['OutputSe']
            self.outputDir = backendDict['OutputDir']#用于outputData
            if 'OutputPath' in backendDict:
                self.outputPath = trimJoinPathElement(backendDict['OutputPath'])
            else:
                self.outputPath = ''
        else:
            self.site = ''
            self.jobGroup = ''
            self.outputSE = ''
            self.outputDir = ''
            self.outputPath = ''
    
    def submit(self,jobSet):
        for jobParam in jobSet:
            result = self._submit(jobParam)
            if result['OK']:
                print 'Job %s submitted successfully. ID = %d' %(jobParam['jobName'],result['Value'])
            else:
                print 'Job %s submitted failed' %jobParam['jobName']
    
    def _submit(self, jobParam):        
        j = Job()
        j.setName(jobParam['jobName'])
        j.setExecutable(jobParam['jobScript'],logFile = jobParam['jobScriptLog'])
        if self.site:
            j.setDestination(self.site)
        if self.jobGroup:
            j.setJobGroup(self.jobGroup)            
        j.setInputSandbox(jobParam['inputSandbox'])
        j.setOutputSandbox(jobParam['outputSandbox'])
        j.setOutputData(jobParam['outputData'], outputSE = self.outputSE, outputPath = self.outputPath)

        dirac = GridDirac()
        result = dirac.submit(j)

        status = {}
        status['submit'] = result['OK']
        if status['submit']:
            status['job_id'] = result['Value']

        return status

    def setSite(self, site):
        self.site = site
        
    def setJobGroup(self, group):
        self.jobGroup = group

    def setOutputSE(self,se):
        self.outputSE = se
        
    def setOutputPath(self,path):
        self.outputPath = path
        
    '''--------------------------------------------------------------------'''       
    def getInputFilePrefix(self,experiment):
        return 'LFN:/%s/lustre-ro' % experiment
    
    def getDFCprefix(self,experiment):
        username = getProxyInfo()['Value']['username']
        initial = username[0]
        prefix = '/%s/user/' % experiment + initial + '/' + username + '/' 
        return prefix
    
    def getOutputDataPath(self,experiment, *args):
        path = os.path.join(self.getDFCprefix(experiment),self.outputDir)
        for each in args:
            path = os.path.join(path,each)
        return 'LFN:'+path
    '''--------------------------------------------------------------------'''
    def registerInputData(self, filepath, size, experiment):
        infoDict = {}
        infoDict['PFN'] = ''
        infoDict['Size'] = size
        infoDict['SE'] = 'IHEP-STORM'
        infoDict['GUID'] = commands.getoutput('uuidgen')
        infoDict['Checksum'] = ''
        fileDict = {}
        lfn =  '/%s/lustre-ro' % experiment + filepath
        fileDict[lfn] = infoDict
        fcc = FileCatalogClient('DataManagement/FileCatalog')
        rm = ReplicaManager()
        result = {}
        result['lfn'] = lfn
        result['is_registered'] = False
        
        #查询
        for repeatTimes in range(10):
            is_registered = fcc.isFile(lfn)
            if (is_registered['OK'] and is_registered['Value']['Successful'].has_key(lfn)):
                break

        if not is_registered['OK']:#查询失败
            result['is_registered'] = 'querry error. unkown'
            print 'Failed to query %s in DFC. Error message is %s' %(lfn, is_registered['Message'])
            
        if is_registered['Value']['Successful'][lfn]:#已注册
            result['is_registered'] = True
            for repeatTimes in range(10):
                is_removed = rm.removeCatalogFile(lfn)#删除
                if (is_removed['OK'] and is_removed['Value']['Successful'][lfn]['FileCatalog']):
                    result['is_removed'] = True
                    break

            if not is_removed['OK']:#删除失败
                result['is_removed'] = 'remove error'
                print 'Failed to remove %s from DFC.' %lfn
        #add       
        for repeatTimes in range(10):
            is_added = fcc.addFile(fileDict)#add/register
            if (is_added['OK'] and is_added['Value']['Successful'][lfn]):
                result['OK'] = True
                return result

        if not is_added['OK']:#add unsuccessfully
            result['OK'] = False
            result['Message'] = is_added['Message']
        elif is_added['Value']['Failed']:
            result['OK'] = False
            result['Message'] = 'Failed to add file' + lfn
        return result
    
    '''----------------------------------------------------------------------------'''
    '''----------------------------------------------------------------------------'''
    def scriptForImport(self):
        return '''from DIRAC.Core.Base import Script
Script.parseCommandLine( ignoreErrors = False )'''
    
    def scriptForJobID(self):
        return '''jobID = os.environ.get('DIRACJOBID', '0')'''
    
    def scriptForSiteName(self):
        return '''from DIRAC import siteName 
siteName = siteName()'''
        
    def scriptForDetermineMirrorDB(self):
        return '''call(['python','determineMirrorDB.py',siteName])\n'''
    
    def scriptForUploadData(self,jobParam):
        return '''\n\'''********************Upload Data********************\'''
        from uploadData import uploadData
        lfns = %s
        se = %s
        for lfn in lfns:
            call(['python','setJobStatus.py',jobID,'CEPC_script','Uploading Data'])
            result = uploadData(lfn, se)
            if not result['OK']:
                try:
                    with open ('job.err','a') as errFile:
                        print>>errFile, 'Upload Data Error:\\n%s' % result
                except IOError as e:
                    print 'IOError:',str(e)\n''' % (jobParam['outputData'],jobParam['se'])