#coding:utf-8
'''
Created on 2015-06-08 16:12:16

@author: suo
'''

class Splitter(object):
    def split(self):
        raise NotImplementedError
        
if __name__ == '__main__':
    aString = 'Chinese'
    print aString[-len('ese'):]
    print 