#coding:utf-8
'''
Created on 2015-06-09 20:22:39

@author: suo
'''
import os,sys
from core.splitter.Splitter import Splitter

class SplitterByFile(Splitter):
    
    def __init__(self,eventPer = None,seedStart = None,splitterDict = None):
        print 'This is SplitterByFile __init__()'
        if splitterDict:
            self.eventMaxPerJob = splitterDict['EventMaxPerJob']
            self.seedStart = splitterDict['SeedStart']
            if 'InputData' in splitterDict:
                self.setInput(splitterDict['InputData'])
            else:
                print 'No inputData specified in the Splitter!\n'\
                      '[Usage]\n'\
                      '  Splitter:\n'\
                      '    InputData: value'
                sys.exit(1)
        else:
            self.eventMaxPerJob = ''
            self.seedStart = ''
            self.inputDataType = ''
            self.inputData = ''
        if eventPer:
            self.eventMaxPerJob = eventPer
        if seedStart:
            self.seedStart =seedStart
            
    def setInput(self, value):
        if os.path.isfile(value):
            self.inputDataType = 'FileList'
        elif os.path.isdir(value):
            self.inputDataType = 'Dir'
        else:
            print 'Splitter InputData is Invalid, please check'
            sys.exit(1)
        self.inputData = value
         
    def resolveInputFileList(self,filename,prefix = '/cefs/',postfix = '.stdhep'):
        '''如果输入是一个文件的列表, 读取检查, 返回元组列表 [(),(),()] '''
#         if not os.path.isfile(filename):
#             print 'Error: %s is not a file'% filename
#             sys.exit(1)
        fileList = []
        inputDataList = []
        seed = self.seedStart
        index = 1
        try:
            with open(filename) as f:
                for eachline in f:
                    line = eachline.strip()
                    if line == '':
                        pass
                    elif not line.startswith(prefix):
                        print 'WARNNING: this line: %s not in %s, ignored.' % (line, prefix)
                    elif not line[-len(postfix):].lower() == postfix:
                        print 'WARNNING: this line: %s doesn\'t end with %s, ignored.' % (line, postfix)              
                    elif not os.path.isfile(line):
                        print 'WARNNING: this line: %s is not a file' % line
                    elif line not in fileList:
                        fileList.append(line)
                        aDict = {'index':str(index),
                                 'inputFilePath':line,
                                 'inputFileSize':os.path.getsize(line),
                                 'inputFileName':os.path.basename(line),
                                 'eventNum':self.eventMaxPerJob,
                                 'seed':str(seed)}
                        inputDataList.append(aDict)
                        seed+=1
                        index+=1
        except IOError as e:
            print 'IOError: ',str(e)
        
        if len(inputDataList)==0:
            print 'No %s file found in %s' % (postfix,filename)
            sys.exit(1)
        print inputDataList
        return inputDataList
    
    def resolveInputDir(self,inputdir,postfix = '.stdhep'):
#         if not os.path.isdir(inputdir):
#             print '%s is not a directory'% inputdir
#             sys.exit(1)
        inputDataList = []
        seed = self.seedStart
        index = 1
        for directory,subdir,files in os.walk(inputdir):
            for filename in files:
                if filename[-len(postfix):].lower() == postfix:
                    filepath = os.path.join(directory,filename)
                    aDict = {'index':str(index),
                             'inputFilePath':filepath,
                             'inputFileSize':os.path.getsize(filepath),
                             'inputFileName':filename,
                             'eventNum':self.eventMaxPerJob,
                             'seed':str(seed)}
                    inputDataList.append(aDict)
                    seed+=1
                    index+=1
        if len(inputDataList)==0:
            print 'No %s file found in %s' % (postfix,filename)
            sys.exit(1)
        return inputDataList
    
    def split(self):
        if self.inputDataType == 'FileList':
            return self.resolveInputFileList(self.inputData, prefix = '/cefs/', postfix = '.stdhep')
        elif self.inputDataType == 'Dir':
            return self.resolveInputDir(self.inputData, postfix = '.stdhep')
