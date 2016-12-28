import os
import shutil
import errno

from jsub.util import safe_mkdir

class FileSystem(object):
    def __init__(self, param):
        self.__param = param
        self.__content_dir = os.path.expanduser(param.get('dir', '~/jsub/content'))

    def __abs_path(self, task_id, path):
        return os.path.join(self.__content_dir, str(task_id), path)

    def put(self, task_id, src, dst):
        dst_abs = self.__abs_path(task_id, dst)
        dst_dir = os.path.dirname(dst_abs)
        safe_mkdir(dst_dir)
        shutil.copy2(src, dst_abs)

    def put_str(self, task_id, string, dst):
        dst_abs = self.__abs_path(task_id, dst)
        dst_dir = os.path.dirname(dst_abs)
        safe_mkdir(dst_dir)
        with open(dst_abs, 'w') as f:
            f.write(string)

    def get(self, task_id, src, dst):
        src_abs = self.__abs_path(task_id, src)
        dst_dir = os.path.dirname(dst)
        safe_mkdir(dst_dir)
        try:
            shutil.copytree(src_abs, dst)
        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy2(src_abs, dst)
            else:
                raise
