class CompositeString(object):
	def __init__(self,param):
		self.__str = param.get('value')
		self.__length = param.get('length',100000)

		self.__counter = 0

	def next(self):
		self.__counter += 1

		if self.__counter > self.__length:
			raise StopIteration

		value = self.__str
		return {'value': value}		
	
	def length(self):
		return None
