#coding:utf-8
'''
Created on 2015-06-24 11:45:28

@author: suo
'''
import sys
from subprocess import call

siteName = sys.argv[1]

call(['python','tmsg.py','Determine which mirror DB to use'])

if siteName in ['CLOUD.IHEP-OPENSTACK.cn', 'CLOUD.IHEP-OPENNEBULA.cn']:
    #sed -i '/匹配字符串/s/替换源字符串/替换目标字符串/g' filename
    #把211的ip替换为75的
    call(['sed','-i',"'s/202.114.78.211/202.122.37.75/g'",'simu.macro'])
    print 'Use site local DB 202.122.37.75'
else:
    print 'Use default DB 202.114.78.211'