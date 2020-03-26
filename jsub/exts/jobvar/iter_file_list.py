import os 

class IterFileList(object):
	def __init__(self,param):
		self.__filelist = param.get('file_list')
		self.__folder = param.get('folder')
		with open(self.__filelist) as f:
			self.__files = [x for x in f.read().splitlines() if os.path.isfile(x)]

	def next(self):
		if len(self.__files)==0:
			raise StopIteration
	
		path=self.__files.pop(0)
		if self.__folder:
			path=os.path.join(self.__folder, path)		

		return {'value':path}

	def	length(self):
		return None
