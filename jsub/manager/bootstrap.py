import os

from jsub.util import safe_copy

class BootstrapManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def create_bootstrap(self, bootstrap_type, dst_dir):
        bootstrap_dir = self.__ext_mgr.ext_dir('bootstrap', bootstrap_type)
        bootstrap_param = self.__ext_mgr.ext_config('bootstrap', bootstrap_type, 'param')
        executable = bootstrap_param.get('executable', 'run')

        src_exe = os.path.join(bootstrap_dir, executable)
        dst_exe = os.path.join(dst_dir, executable)
        safe_copy(src_exe, dst_exe)

        with open(os.path.join(dst_dir, 'executable'), 'w') as f:
            f.write(executable)
