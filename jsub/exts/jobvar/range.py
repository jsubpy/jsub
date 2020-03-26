class Range(object):
    def __init__(self, param):
        self.__first  = param.get('first', 1)
        self.__last   = param.get('last')
        self.__step   = param.get('step',  1)
        self.__length = param.get('length',100000)

        self.__value   = self.__first
        self.__counter = 0

    def next(self):
        if self.__last and (self.__value-self.__last)*self.__step > 0:
            raise StopIteration

        self.__counter += 1
        if self.__length and self.__counter > self.__length:
            raise StopIteration

        value = self.__value
        self.__value += self.__step
        return {'value': value}

    def length(self):
        return None
