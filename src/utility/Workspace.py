#coding:utf-8
'''
Created on 2015-06-30 23:49:50

@author: suo
'''
import os
'''创建任务master目录，序号递增'''
def createMasterRepoDir(repoDirRoot):#yant/dsub/0.1/doc/dsub-example/repo/
    repoDir = os.path.join(repoDirRoot, 'workspace')
    if not os.path.isdir(repoDir):
        os.mkdir(repoDir)
    masterDir = os.path.join( repoDir, repr(len(os.listdir(repoDir))) )#根据当前文件(夹)数目创建,递增
    os.mkdir(masterDir)
    return masterDir#workspace/1/