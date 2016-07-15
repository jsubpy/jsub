import sys,yaml

sys.path.append(object)
print sys.path

try:
    with open('CepcJob.yaml') as f:
        x = yaml.load(f)
except Exception as e:
    print 'Exception: ',str(e)
else:
    print x['Experiment']['Name']
    print x['Splitter']['Type']
    
x = {'name':'bing','age':'20'}

y = {'gender':'male'}

x.update(y)
print x

x=None
if x:
    print 'X is not none'
    
    
if 1:
    print '1'
if 0:
    print '0'