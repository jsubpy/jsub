#coding:utf-8
'''
Created on 2015-06-15 19:10:54

@author: suo
'''
import os,shutil
try:
    import xml.etree.cElementTree as ET
except ImportError:
    #import xml.etree.ElementTree as ET
    import lxml.etree as ET
    
from core.OptionsParser import OptionsParser

class CepcRecParser(OptionsParser):
    
    def __init__(self, opts):
        super(CepcRecParser, self).__init__(opts)
        for each in self.opts:
            if os.path.isfile(each) and os.path.basename(each)=='reco.xml':
                self.reco_xml = each
            elif os.path.isfile(each) and os.path.basename(each)=='PandoraLikelihoodData9EBin.xml':
                self.likelihood_data = each
            elif os.path.isfile(each) and os.path.basename(each)=='PandoraSettingsDefault.xml':
                self.settings_default = each
            else:
                print 'Invalid options file: ', each
        self.pandolaFlag = 0
        
    def __generatePandoras(self,masterdir):
        #----------------------PandoraLikehoodData 不用改,直接拷贝到master下
        shutil.copy(self.likelihood_data, masterdir)
        
        #----------------------PandoraSettingsDefault 改, 写到master下
        pandoraSD = ET.parse(source = self.settings_default)
        for element in pandoraSD.findall('algorithm/HistogramFile'):
            element.text = 'PandoraLikelihoodData9EBin.xml'
        pandoraSD.write(os.path.join(masterdir, 'PandoraSettingsDefault.xml'))
        
    def __prepareRecoXml(self):
        recoXML = ET.parse(source = self.reco_xml)
        for element in recoXML.findall('processor/parameter[@name="PandoraSettingsXmlFile"]'):
            element.text = 'PandoraSettingsDefault.xml'
        return recoXML
    
    def __generateRecoXml(self,subdir,template,inputFilenamePre):#待改，sim可能不做，输入文件名无法这样写
        for element in template.findall('global/parameter[@name="LCIOInputFiles"]'):
            element.text = inputFilenamePre + '_sim.slcio'
        for element in template.findall('processor[@name="MyLCIOOutputProcessor"]/parameter[@name="LCIOOutputFile"]'):
            element.text = inputFilenamePre + '_rec.slcio'
        destination = os.path.join(subdir, 'reco.xml')
        try:
            with open(destination,'w'):
                template.write(destination)
        except IOError as err:
            print "InitXml:",str(err)
         
    def parse(self):
        print 'Enter CepcRecParser.parse()'
        self.recoTemplate = self.__prepareRecoXml()
    
    def generateOpts(self, **kwargs):
        if 'masterDir' not in kwargs:
            print 'masterDir not specified'
        elif 'subDir' not in kwargs:
            print 'subDir not specified'
        elif 'inputFileName' not in kwargs:
            print 'inputFileName not specified'
        else:
            if not self.pandolaFlag:#只需执行一次
                self.__generatePandoras(kwargs['masterDir'])
                self.pandolaFlag = 1
            self.__generateRecoXml(kwargs['subDir'], self.recoTemplate, os.path.splitext(kwargs['inputFileName'])[0])