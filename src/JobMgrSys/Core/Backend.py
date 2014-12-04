from .Entity import Entity

class Backend(Entity):
    def setEnv(self):
        pass

    def submit(self, param):
        raise Exception('not implemented')
