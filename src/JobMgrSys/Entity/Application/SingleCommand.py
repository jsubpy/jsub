from ...Core.Application import Application

class SingleCommand(Application):
    def __init__(self):
        Application.__init__(self)
        self.setParam('name', self.getName())
        self.setArgs()

    def setCommand(self, command):
        self.setParam('command', command)

    def setArgs(self, args=[]):
        self.setParam('args', args)
