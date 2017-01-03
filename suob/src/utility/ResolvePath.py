'''
Created on 2015-07-14 00:37:24

@author: suo
'''

def trimJoinPathElement(filepath):
    '''get rid of / at the beginning of filepath'''
    while filepath.startswith('/'):
        filepath = filepath[1:]
    return filepath

# path = '//cepc/test/s'
# print trimJoinPathElement(path)