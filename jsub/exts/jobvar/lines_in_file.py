import os

class LinesInFile(object):
	def __init__(self, param):
		self.__file = param.get('file')
	
		with open(self.__file) as f:
			self.__lines = [x for x in f.read().splitlines()]
	
	def next(self):
		if len(self.__lines)==0:
			raise StopIteration

		line=self.__lines.pop(0)

		return {'value':line}

	def length(self):
		return None
