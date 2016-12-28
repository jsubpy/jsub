from jsub.error import SplitterParamError

class Sequence(object):
    def __init__(self, param):
        if 'last' not in param:
            raise SplitterParamError('Parameter not found: "last"')

        self.__first = param.get('first', 1)
        self.__last  = param['last']
        self.__step  = param.get('step',  1)

        self.__value = self.__first

    def next(self):
        if self.__value > self.__last:
            raise StopIteration
        value = self.__value
        self.__value += self.__step
        return {'value': value}
