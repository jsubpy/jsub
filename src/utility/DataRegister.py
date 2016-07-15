#coding:utf-8
'''
Created on 2015-06-30 17:12:08

@author: suo
'''
import commands
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC.DataManagementSystem.Client.ReplicaManager import ReplicaManager

def registerInputData(filepath, size, prefix = '/cepc/lustre-ro'):
    infoDict = {}
    infoDict['PFN'] = ''
    infoDict['Size'] = size
    infoDict['SE'] = 'IHEP-STORM'
    infoDict['GUID'] = commands.getoutput('uuidgen')
    infoDict['Checksum'] = ''
    fileDict = {}
    lfn =  prefix + filepath
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
#         else:
#             continue
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
#             else:
#                 continue
        if not is_removed['OK']:#删除失败
            result['is_removed'] = 'remove error'
            print 'Failed to remove %s from DFC.' %lfn
    #add       
    for repeatTimes in range(10):
        is_added = fcc.addFile(fileDict)#add/register
        if (is_added['OK'] and is_added['Value']['Successful'][lfn]):
            result['OK'] = True
            return result
#         else:
#             continue
    if not is_added['OK']:#add unsuccessfully
        result['OK'] = False
        result['Message'] = is_added['Message']
    elif is_added['Value']['Failed']:
        result['OK'] = False
        result['Message'] = 'Failed to add file' + lfn
    return result