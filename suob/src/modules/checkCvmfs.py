#coding:utf-8
'''
Created on 2015-05-19 22:23:57

@author: suo
'''
import os,sys
from subprocess import call

cvmfsPath = sys.argv[1]
'''version Zhao'''
# try:
#     os.listdir(cvmfsPath)
# except OSError as err:
#     try:
#         with open('job.err', 'a') as errFile:
#             print >> errFile, 'List directory "%s" failed: %s' % (sys.argv[1],str(err))
#     except IOError as e:
#         print 'IOError: ',str(e)
# 
# if not os.path.isdir(cvmfsPath):
#     call(['python','setJobStatus.py',jobID,'CEPC_script','cvmfs not found'])
#     sys.exit(11)
#--------------------------------------------------------------------------   
'''version Yan'''
call(['python','tmsg.py','Check cvmfs'])

for repeatTimes in range(10):
    found_cvmfs = not call(['ls',cvmfsPath])#找到的话,found_cvmfs == 1
    if found_cvmfs:
        break
    else:
        call(['sleep','5'])
if not found_cvmfs:
    sys.exit(11)