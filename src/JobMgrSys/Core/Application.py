from .Entity import Entity
from .Parameter import Parameter

class Application(Entity):
    def __init__(self):
        self.__param = {}

    def initialize(self):
        pass

    def getParam(self):
        return self.__param

    def setParam(self, key, value):
        self.__param[key] = value
