'''
Created on 2015-06-30 17:36:47

@author: suo
'''
import random,sys
from subprocess import call

max_q_time = int(sys.argv[1])
jobID = sys.argv[2]
description = sys.argv[3]

if max_q_time != 0:
    q_time = max_q_time * random.random()
    q_msg = 'Queue for %.2f seconds' %q_time
    call(['python','tmsg.py',q_msg])
    call(['python','setJobStatus.py',jobID,description,q_msg])
    
    call(['sleep','%f'%q_time])
    
    call(['python','tmsg.py','End queue'])