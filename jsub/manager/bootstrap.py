import os

from jsub.util import safe_copy

class BootstrapManager(object):
    def __init__(self, jsub_root_dir):
        self.__jsub_root_dir = jsub_root_dir

    def create_bootstrap(self, dst_dir):
        file_name = 'bootstrap.sh'
        safe_copy(os.path.join(self.__jsub_root_dir, 'bootstrap', file_name), os.path.join(dst_dir, file_name))
