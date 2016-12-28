import os

from jsub.util import safe_copy

class NavigatorManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def __nav_scenario(self, navigator):
        pass

    def create_navigators(self, navigators, dst_dir):
        navigator_dirs = {}
        for navigator in navigators:
            navigator_dirs[navigator] = self.__ext_mgr.ext_dir('navigator', navigator)

        digit_number = len(str(len(navigator_dirs)))
        navigator_format = '%%0%dd-%%s' % max(digit_number, 2)
        navigator_index = 1
        for name, path in navigator_dirs.items():
            src = os.path.join(path, 'run')
            indexed_name = navigator_format % (navigator_index, name)
            dst = os.path.join(dst_dir, indexed_name, 'run')
            safe_copy(src, dst)
            navigator_index += 1

    def scenario_format(self, navigators):
        for navigator in navigators:
            navigator_dir = self.__ext_mgr.ext_dir('navigator', navigator)
