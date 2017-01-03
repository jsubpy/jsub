#coding:utf-8
'''
Created on 2015-05-20 00:01:24

@author: suo
'''
import sys,pprint
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC.DataManagementSystem.Client.ReplicaManager import ReplicaManager

'''discarded module, uploadData is used'''
def checkOutputData(lfnx):
    fcc = FileCatalogClient('DataManagement/FileCatalog')
    rm = ReplicaManager()
    result = {}
    lfn = lfnx[4:]
    result['lfn'] = lfn
    result['is_registered'] = False
    result['is_removed'] = False
    result['query_OK'] = True
    try:
        with open('job.err','a+') as errFile, open('job.log','a+') as logFile: 
            for repeatTimes in range(10):
                is_registered = fcc.isFile(lfn)
                if (is_registered['OK'] and is_registered['Value']['Successful'].has_key(lfn)):
                    break#查询成功&&已注册
                
            if not is_registered['OK']:#查询失败,直接返回
                result['query_OK'] = False
                print >> errFile, 'Failed to query %s in DFC. Error message is %s' %(lfn, is_registered['Message'])
                return result
            else:#查询成功
                print >> logFile, 'Query successfully. OutputData registered info is:'
                pprint(is_registered, logFile)#将集合元素逐行显示
                
            if is_registered['Value']['Successful'][lfn]:#已注册
                result['is_registered'] = True
                for repeatTimes in range(10):
                    is_removed = rm.removeCatalogFile(lfn)#删除...
                    if (is_removed['OK'] and is_removed['Value']['Successful'][lfn]['FileCatalog']):
                        result['is_removed'] = True
                        print >> logFile, '%s is removed from DFC' %lfn
                        break
                    else:
                        continue
                if not is_removed['OK']:#未删除成功
                    print >> errFile, 'Failed to remove %s from DFC. Error message is %s' %(lfn, is_removed['Message'])
            else:#未注册
                print >> logFile, '%s is not registered. Nothing to do.' %lfn
            print >> logFile, 'result of dfc check is:'
            pprint(result, logFile)
            print >> logFile, '  '
    except IOError as e:
        print 'IOError: ',str(e)
    
    return result