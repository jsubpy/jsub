import random

class Randint(object):
	def __init__(self, param):
		self.__min   = param.get('min',0)
		self.__max   = param.get('max',  2000000000)
		self.__length = param.get('length',100000)

		self.__value   = self.__length
		self.__counter = 0

	def next(self):

		self.__counter += 1
		if self.__length and self.__counter > self.__length:
			raise StopIteration

		value=random.randint(int(self.__min),int(self.__max))
		return {'value': value}

	def length(self):
		return self.__length
