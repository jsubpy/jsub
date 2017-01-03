'''
Created on 2015-05-19 21:45:37

@author: suo
'''
import sys
from DIRAC.WorkloadManagementSystem.Client.JobReport import JobReport
from DIRAC.Core.Base import Script
Script.parseCommandLine( ignoreErrors = False )

jobID = sys.argv[1]
experiment = sys.argv[2]
message = sys.argv[3]

jobReport = JobReport(jobID,experiment)
result = jobReport.setApplicationStatus(message)
if not result['OK']:
    try:
        with open('job.err','a') as errFile: 
            print >> errFile, 'setJobStatus error: %s' % result
    except IOError as e:
        print 'IOError:',str(e)
