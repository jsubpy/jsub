class Common(object):
    def __init__(self, param):
        self.__param = param

    def build(self, backend):
        return self.__param
