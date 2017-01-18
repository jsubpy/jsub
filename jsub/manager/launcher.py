import os

from jsub.util import safe_copy

class LauncherManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def create_launcher(self, launcher_type, dst_dir):
        launcher_dir = self.__ext_mgr.ext_dir('launcher', launcher_type)
        launcher_param = self.__ext_mgr.ext_config('launcher', launcher_type, 'param')
        executable = launcher_param.get('executable', 'launcher')

        src_exe = os.path.join(launcher_dir, executable)
        dst_exe = os.path.join(dst_dir, executable)
        safe_copy(src_exe, dst_exe)

        return executable
