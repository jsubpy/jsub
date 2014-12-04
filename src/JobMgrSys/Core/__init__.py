import os

from .Job import Job

gSysParam = {}

class Program:
    def __init__(self, argv=[]):
        self.__argv = argv
        self.__parseCommand()
        self.__setSysParam()

    def __parseCommand(self):
        if self.__argv:
            self.__script = self.__argv[0]

    def __setSysParam(self):
        script_name = os.path.basename(os.path.normpath(self.__script))
        script_dir = os.path.dirname(os.path.abspath(os.path.normpath(self.__script)))
        script_param = {'cwd': os.getcwd(), 'script': {'name': script_name, 'dir': script_dir}}
        gSysParam.update(script_param)

    def run(self):
        j = Job()

        if self.__script:
            execfile(self.__script)
