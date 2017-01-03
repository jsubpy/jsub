#coding:utf-8
'''
Created on 2014-12-19 06:29:16

@author: SUO Bing
'''
import os,tarfile

def tarDir(src,dst):
    tar=tarfile.open(dst,"w:gz")
    for root,dir,files in os.walk(src):
        for file in files:
            fullpath=os.path.join(root,file)
            tar.add(fullpath,arcname=os.path.basename(root)+"/"+os.path.basename(fullpath))
    tar.close()
    
if __name__ == '__main__':
    src = os.path.join('/home/suo','template/')#加/和不加/是不一样的
    dst = os.path.join('/home/suo','template.tgz')
    tarDir(src, dst)