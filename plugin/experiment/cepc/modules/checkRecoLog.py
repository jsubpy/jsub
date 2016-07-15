'''
Created on 2015-06-25 12:26:46

@author: suo
'''
import sys
from subprocess import call
eventNum = sys.argv[1]
# jobID = sys.argv[2]
sInfo = 'MyLCIOOutputProcessor: %s events in 1 runs written to file' % eventNum
'''直接用grep <String> file'''
try:
    with open('reco.log') as recoLog:
        recoLogfind = False
        for line in recoLog:
            if line.find(sInfo) != -1:
                recoLogfind = True
                break
        if not recoLogfind:
            sys.exit(30)
except IOError as err:
    print 'IOError ',str(err)