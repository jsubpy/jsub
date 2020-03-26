import os

from jsub.util import safe_copy

class NavigatorManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def __nav_param(self, navigator_type):
        return self.__ext_mgr.ext_config('navigator', navigator_type, 'param')

    def context_format(self, navigators):
        formats = []
        for navigator_type in navigators:
            nav_param = self.__nav_param(navigator_type)
            fmt = nav_param.get('context_format', ['py'])
            formats += fmt if isinstance(fmt, list) else [fmt]
        return formats

    def create_navigators(self, navigators, dst_dir):
        for navigator_type in navigators:
            nav_dir = self.__ext_mgr.ext_dir('navigator', navigator_type)
            nav_param = self.__nav_param(navigator_type)
            executable = nav_param.get('executable', 'navigator')

            src_exe = os.path.join(nav_dir, executable)
            dst_exe = os.path.join(dst_dir, navigator_type, executable)
            safe_copy(src_exe, dst_exe)

            with open(os.path.join(dst_dir, navigator_type, 'executable'), 'w') as f:
                f.write(executable)

        with open(os.path.join(dst_dir, 'navigator.list'), 'w') as f:
            for navigator_type in navigators:
                f.write(navigator_type)
                f.write('\n')
