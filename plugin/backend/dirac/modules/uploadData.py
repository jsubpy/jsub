#coding:utf-8
'''
Created on 2015-06-25 16:50:18

@author: suo
'''
import os,time,random
from DIRAC.Interfaces.API.Dirac import Dirac
dirac = Dirac()
from DIRAC import S_OK, S_ERROR, gConfig
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC.Core.Base import Script
Script.parseCommandLine( ignoreErrors = False )
fccType = 'DataManagement/FileCatalog'
fcc = FileCatalogClient(fccType)

def uploadData(lfn, se):
    removeData(lfn)
    try:
        with open('job.log','a') as logFile, open('job.err','a') as errFile:  
            path = os.path.basename(lfn)  
            for i in range(0, 5):
                result = dirac.addFile(lfn, path, se)#为什么要用dirac???
                if result['OK'] and result['Value']['Successful'] and result['Value']['Successful'].has_key(lfn):
                    break
                time.sleep(random.randint(180, 600))
                print >>errFile, '- Upload to %s on SE %s failed, try again' % (lfn, se)
            if result['OK']:
                if result['Value']['Successful'] and result['Value']['Successful'].has_key(lfn):
                    print >>logFile, 'Successfully uploading %s to %s. Retry %s' % (lfn, se, i+1)
                    return result
                else:#OK,但没Successful
                    print >>errFile, 'Failed type 2 uploading %s to %s. Retry %s' % (lfn, se, i+1)
                    return S_ERROR('Upload to %s on SE %s failed' % (lfn, se))
            else:#没OK
                print >>errFile, 'Failed type 1 uploading %s to %s. Retry %s' % (lfn, se, i+1)
                return result
    except IOError as e:
        print 'IOError:',str(e)
        
def removeData(lfn):
    try:
        with open('job.log','a') as logFile, open('job.err','a') as errFile:
            result = fcc.isfile(lfn)
            if not (result['OK'] and lfn in result['Value']['Successful'] and result['Value']['Successful'][lfn]):
                return result
        
            for i in range(0, 16):
                try:
                    result = fcc.removeFile(lfn)
                    if result['OK'] and result['Value']['Successful'] and result['Value']['Successful'].has_key(lfn):
                        break
                except Exception, e:
                    result = S_ERROR('Exception: %s' % str(e))
                    break
                time.sleep(random.randint(6, 30))
                print >>errFile, '- Remove %s failed, try again' % lfn
            if result['OK']:
                if result['Value']['Successful'] and result['Value']['Successful'].has_key(lfn):
                    print >>logFile, 'Successfully remove %s. Retry %s' % (lfn, i+1)
                    return result
                else:
                    print >>errFile, 'Failed type 2 remove %s. Retry %s' % (lfn, i+1)
                    return S_ERROR('Remove %s failed' % lfn)
            else:
                print >>errFile, 'Failed type 1 remove %s. Retry %s' % (lfn, i+1)
                return result
    except IOError as e:
        print 'IOError:',str(e)