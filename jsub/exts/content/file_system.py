import os
import shutil

def _mkdir_p(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

class FileSystem(object):
    def __init__(self, param):
        self.__param = param
        self.__content_dir = os.path.expanduser(param.get('dir', '~/jsub/content'))

    def put(self, task_id, content_type, src, dst):
        dst_abs = os.path.join(self.__content_dir, str(task_id), content_type, dst)
        dst_dir = os.path.dirname(dst_abs)
        _mkdir_p(dst_dir)
        shutil.copy2(src, dst_abs)
