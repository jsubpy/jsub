#!/usr/bin/env python

#register files to LFN;
#if files are not under /cefs; copy to /cefs/dirac/user/{first-char}/{user-name}/jsub/{mother-dir}/ (don't append full path because of max depth limit of LFN)
#LFN = /{vo}/user/{first-char}/{user-name}/ + full_path


import os

from DIRAC import S_OK, S_ERROR, gLogger, exit
from DIRAC.Core.Base import Script

Script.setUsageMessage('Register files to DFC')
Script.parseCommandLine(ignoreErrors=False)

from DIRAC.Core.Utilities.Adler import fileAdler
from DIRAC.Core.Utilities.File import makeGuid
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
from DIRAC.Core.Security.ProxyInfo import getProxyInfo
from DIRAC.ConfigurationSystem.Client.Helpers import Registry


from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
fcc = FileCatalogClient('DataManagement/FileCatalog')

files = Script.getPositionalArgs()

_bufferSize = 100
_se = 'IHEP-STORM'
overwrite=False



def main():
	dm = DataManager()

	fileTupleBuffer = []

	res = getProxyInfo( False, False )
	if not res['OK']:
		gLogger.error( "Failed to get client proxy information.", res['Message'] )
		DIRAC.exit( 2 ) 
	proxyInfo = res['Value']
	owner = res['Value']['username']
	ownerGroup = res['Value'].get('group')
	if proxyInfo['secondsLeft'] == 0:
		gLogger.error( "Proxy expired" )
		DIRAC.exit( 2 ) 
	vo = ''
	if 'group' in proxyInfo:
		vo = Registry.getVOMSVOForGroup(ownerGroup)

	voHome = '/{0}'.format(vo)
	userHome = '/{0}/user/{1:.1}/{1}'.format(vo, owner)



	counter = 0
	for f in files:
		counter += 1
		local_f=f
		if not f.startswith('/cefs'):
#			gLogger.error('File must be under "/cefs"')
#			continue

		#if the file to reg is not under /cefs, use put and register
#			lfn = '/cepc/user/%s/%s/jsub/'%(username[0],username) + folder_name + '/' + os.path.basename(f)
			f2=f
			if f2.startswith('/'):
				f2=f2[1:]
			lfn = os.path.join(userHome,f2)

#			dirname = os.path.dirname(local_f)
#			os.system('mkdir -p %s'%(dirname))
#			os.system('cp %s %s' %(f,local_f))
			do_put_and_register=True
		else: 
			lfn = '/cepc/lustre-ro' + os.path.abspath(f)
#			lfn =os.path.join('/',vo, os.path.abspath(f)[1:])
			do_put_and_register=True

		result = fcc.isFile(lfn)
		if result['OK'] and lfn in result['Value']['Successful'] and result['Value']['Successful'][lfn]:
			continue

		size = os.path.getsize(f)
		adler32 = fileAdler(f)
		guid = makeGuid()
		fileTuple = (lfn, local_f, size, _se, guid, adler32)
		fileTupleBuffer.append(fileTuple)
		gLogger.debug('Register to lfn: %s' % lfn)
		gLogger.debug('fileTuple: %s' % (fileTuple,))

		if len(fileTupleBuffer) >= _bufferSize:
			if do_put_and_register:
				result = dm.putAndRegister(lfn, local_f, _se, guid, overwrite=overwrite)
			else:
				result = dm.registerFile(fileTupleBuffer)
			print('register result', result)
			if not result['OK']:
				gLogger.error('Register file failed')
				return 1
			del fileTupleBuffer[:]
			gLogger.debug('%s files registered' % counter)

	if fileTupleBuffer:
		if do_put_and_register:
			result = dm.putAndRegister(lfn, local_f, _se, guid, overwrite=overwrite)
		else:
			result = dm.registerFile(fileTupleBuffer)
		print('register result', result)
		if not result['OK']:
			gLogger.error('Register file failed')
			return 1
		del fileTupleBuffer[:]

	gLogger.info('Totally %s files registered' % counter)
	return 0


if __name__ == '__main__':
	exit(main())
