'''
Created on 2015-05-19 22:48:41

@author: suo
'''
from subprocess import call

call(['python','tmsg.py','check execute environment'])

call(['hostname'])
call(['date'])
call(['uname','-a'])