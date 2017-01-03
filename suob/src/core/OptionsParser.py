'''
Created on 2015-06-11 20:44:31

@author: suo
'''
import copy

class OptionsParser(object):
    
    def __init__(self, opts = None):
        if opts!=None:
            self.opts = copy.deepcopy(opts)
            
    def parse(self):
        '''This method will parse the options files and generate 
        necessary opts for each subjob. It must be implemented.'''
        raise NotImplementedError
    
    def generateOpts(self, **kwargs):
        '''This method will generate necessary opts file for each subjob, 
        it should be called after parse(). It must be implemented.
        @param **kwargs: dynamic params which will appear differently when subclass object call it.
        '''
        raise NotImplementedError