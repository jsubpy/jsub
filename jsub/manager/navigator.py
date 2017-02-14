import os

from jsub.util import safe_copy

class NavigatorManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def __nav_param(self, navigator_type):
        return self.__ext_mgr.ext_config('navigator', navigator_type, 'param')

    def scenario_format(self, navigators):
        formats = []
        for navigator_type in navigators:
            nav_param = self.__nav_param(navigator_type)
            fmt = nav_param.get('scenario_format', ['py'])
            formats += fmt if isinstance(fmt, list) else [fmt]
        return formats

    def create_navigators(self, navigators, dst_dir):
        digit_number = len(str(len(navigators) - 1))
        navigator_format = '%%0%dd-%%s' % max(digit_number, 2)
        navigator_index = 0
        for navigator_type in navigators:
            nav_dir = self.__ext_mgr.ext_dir('navigator', navigator_type)
            nav_param = self.__nav_param(navigator_type)
            executable = nav_param.get('executable', 'navigator')

            src_exe = os.path.join(nav_dir, executable)
            indexed_name = navigator_format % (navigator_index, navigator_type)
            dst_exe = os.path.join(dst_dir, indexed_name, executable)
            safe_copy(src_exe, dst_exe)

            with open(os.path.join(os.path.join(dst_dir, indexed_name), 'executable'), 'w') as f:
                f.write(executable)

            navigator_index += 1
