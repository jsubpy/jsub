import logging

class PackageManager(object):
    def __init__(self, packages):
        self.__packages = packages

        self.__logger = logging.getLogger('JSUB')

    def load_config(self, package):
        pass

    def packages(self):
        return self.__packages
