#!/usr/bin/env python
import sys,os
from subprocess import call
from DIRAC import siteName

# logFile = open('job.log', 'w')
# errFile = open('job.err', 'w')
'''********************Preparation********************'''
jobID = os.environ.get('DIRACJOBID', '0')
siteName = siteName()

call(['python','checkExeEnv.py'])

result = call(['python','checkCvmfs.py','/cvmfs/cepc.ihep.ac.cn/',jobID])
if result!=0:
    sys.exit(result)

call(['python','listInputSanbox.py'])

call(['python','determineMirrorDB.py',siteName])
max_q_time = 60 * 5
call(['python','determineQueue.py',siteName,max_q_time])

'''********************Execute Simulation********************'''
call(['python','tmsg.py','Generate shell script for simulation'])
call(['chmod','755','simu.sh'])
call(['python','setJobStatus.py',jobID,'CEPC_script','Mokka Simulation'])
call(['python','tmsg.py','Start simulation'])
result = call(['./simu.sh','Mokka'])

call(['python','checkSimuLog.py',result])

'''********************Execute Reconstruction********************'''
call(['python','tmsg.py','Generate shell script for reconstruction'])
call(['chmod','755','reco.sh'])
call(['python','setJobStatus.py',jobID,'CEPC_script','Marlin Reconstruction'])
call(['python','tmsg.py','Start reconstruction'])
call(['./reco.sh','Marlin'])

call(['python','checkRecoLog.py',10])

'''********************Upload Data********************'''
from uploadData import uploadData
lfns = 111
se = IHEP
for lfn in lfns:
    call(['python','setJobStatus.py',jobID,'CEPC_script','Uploading Data'])
    result = uploadData(lfn, se)
    if not result['OK']:
        try:
            with open ('job.err','a') as errFile:
                print>>errFile, 'Upload Data Error:\n%s' % result
        except IOError as e:
            print 'IOError:',str(e)
'''********************Job Completed********************'''
call(['python','tmsg.py','Job Completed. Files in current dir:'])
call(['ls','-l'])
call(['python','setJobStatus.py',jobID,'CEPC_script','Done'])
call(['python','tmsg.py','Job Done'])
# logFile.close()
# errFile.close()
