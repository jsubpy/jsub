class Enumerate(object):
	def __init__(self, param):
		self.__list = param.get('value')
		self.__list = param.get('list',self.__list)
	
	def next(self):
		if len(self.__list)==0:
			raise StopIteration

		value=self.__list.pop(0)		

		return {'value':value}		

	def length(self):
		return None
