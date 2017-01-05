import os

from jsub.util import safe_copy

from jsub.config import load_config_file

class BootstrapManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def __bootstrap_config(self, bootstrap_dir):
        bootstrap_config_file = os.path.join(bootstrap_dir, 'config.yml')
        return load_config_file(bootstrap_config_file)

    def create_bootstrap(self, bootstrap, dst_dir):
        bootstrap_dir = self.__ext_mgr.ext_dir('bootstrap', bootstrap)
        bootstrap_config = self.__bootstrap_config(bootstrap_dir)
        executable = bootstrap_config.get('executable', 'run')

        src_exe = os.path.join(bootstrap_dir, executable)
        dst_exe = os.path.join(dst_dir, 'bootstrap')
        safe_copy(src_exe, dst_exe)
