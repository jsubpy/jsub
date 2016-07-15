#coding:utf-8
'''
Created on 2015-06-11 22:18:38

@author: suo
'''
import os
from core.OptionsParser import OptionsParser

class CepcSimParser(OptionsParser):
    
    def __init__(self,opts,mirrorDB):
        super(CepcSimParser, self).__init__(opts)
        for each in self.opts:
            if os.path.isfile(each) and os.path.basename(each)=='simu.macro':
                self.simu_macro = each
            elif os.path.isfile(each) and os.path.basename(each)=='event.macro':
                self.event_macro = each
            else:
                print 'Invalid options file: ',each
        self.mirrorDB = mirrorDB
    '''_prepare方法读取模板文件,返回[],存到成员变量中,可能会替换部分公有参数;只在master中调用
       _generate方法根据模板和subjob参数,替换各自参数;在sub中循环调用
    '''            
    def __prepareEventMacro(self):
        template = []
        try:
            with open(self.event_macro) as f:
                for eachLine in f:
                    trimedLine = eachLine.lstrip()
                    if trimedLine == '' or trimedLine.startswith('#'):
                        continue
                    else:
                        template.append(trimedLine)
        except IOError as e:
            print 'IOError: ', str(e)
        return template
    
    def __generateEventMacro(self,subdir,template,eventNum,inputFilename):
        try:
            with open(os.path.join(subdir,'event.macro'),'w') as f:
                for line in template:
                    if line.startswith('/generator/generator'):
                        f.write('/generator/generator '+inputFilename+'\n')
                    elif line.startswith('/run/beamOn'):
                        f.write('/run/beamOn '+ repr(eventNum)+'\n')
                    else:
                        f.write(line)
        except IOError as e:
            print 'IOError: ', str(e)
            
    def __prepareSimuMacro(self):
        template = []
        try:
            with open(self.simu_macro) as f:
                for eachLine in f:
                    trimedLine = eachLine.lstrip()
                    if (trimedLine == '' or trimedLine.startswith('#')):
                        continue
                    #'''设置mirrorDB,或者设为指定值,或者不动'''
                    elif trimedLine.startswith('/Mokka/init/dbHost') and self.mirrorDB:
                        template.append('/Mokka/init/dbHost %s\n'%self.mirrorDB)
                    elif trimedLine.startswith('/Mokka/init/initialMacroFile'):
                        template.append('/Mokka/init/initialMacroFile event.macro\n')
                    else:
                        template.append(trimedLine)
        except IOError as e:
            print 'IOError :',str(e)
        return template
    
    def __generateSimuMacro(self,subdir, template, inputFilenamePre):
        try:
            with open(os.path.join(subdir, 'simu.macro'), 'w') as f:
                for line in template:
                    if line.startswith('/Mokka/init/lcioFilename'):
                        f.write('/Mokka/init/lcioFilename ' + inputFilenamePre + '_sim.slcio\n')
                    else:
                        f.write(line)
        except IOError as e:
            print 'IOError: ',str(e)
            
    def parse(self):
        '''解析结果存到对象属性中'''
        print 'Enter CepcSimParser.parse()'
        self.eventTemplate = self.__prepareEventMacro()
        self.simuTemplate  = self.__prepareSimuMacro()
    
    def generateOpts(self, **kwargs):#用得着**吗...
        if 'subDir' not in kwargs:
            print 'subDir not specified'
        elif 'eventNum' not in kwargs:
            print 'eventNum not specified'
        elif 'inputFileName' not in kwargs:
            print 'inputFileName not specified'
        else:
            self.__generateEventMacro(kwargs['subDir'], self.eventTemplate, kwargs['eventNum'], kwargs['inputFileName'])
            self.__generateSimuMacro(kwargs['subDir'], self.simuTemplate, os.path.splitext(kwargs['inputFileName'])[0])
        
if __name__ == '__main__':
    parser = CepcSimParser(['/home/suo/template/simu.macro','/home/suo/template/event.macro'])
    from optionsParser.CepcRecParser import CepcRecParser
    parser2= CepcRecParser(['/home/suo/template/reco.xml','/home/suo/template/PandoraLikelihoodData9EBin.xml','/home/suo/template/PandoraSettingsDefault.xml'])

    parser.parse()#解析options文件, 结果存到parser的实例属性中
    parser2.parse()
    
    from splitters.SplitterByFile import SplitterByFile
    for filepath, filesize, filename in SplitterByFile().split():#对拆分得到的每项, 生成
        jobPara = {'masterdir':'','subdir':'','eventNum':10,'inputFilename':filename}
        parser.generateOpts(**jobPara)
        parser2.generateOpts(**jobPara)