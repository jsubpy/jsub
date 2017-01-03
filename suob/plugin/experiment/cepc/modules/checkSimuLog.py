'''
Created on 2015-06-25 12:54:49

@author: suo
'''
import sys
from subprocess import call
result = sys.argv[1]

if result!=0:#sim.sh executed failed
    if call(['grep','Database connection failed', 'simu.log'])!=0:
        sys.exit(21)
    sys.exit(20)