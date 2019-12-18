import os

class AllFilesInFolder(object):
	def __init__(self,param):
		self.__path = param.get('path','./')
		self.__suffix = param.get('suffix')
		self.__keyword = param.get('keyword')


		#get all files in path, and filter
		self.__files=[f for f in  os.listdir(self.__path) if os.path.isfile(os.path.join(self.__path,f))]
		if self.__keyword:
			self.__files=[f for f in self.__files if self.__keyword in f]
		if self.__suffix:
			self.__files=[f for f in self.__files if f.endswith(self.__suffix)]

	def next(self):
		if len(self.__files)==0:
			raise StopIteration
	
		path=os.path.join(self.__path,self.__files.pop(0))		

		return {'value':path}

	def	length(self):
		return None
