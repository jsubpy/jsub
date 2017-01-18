class BackendManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def property(self, backend_data):
        backend = self.__ext_mgr.load_ext_common('backend', backend_data)
        return backend.property()

    def work_root(self, backend_data, task_id):
        backend = self.__ext_mgr.load_ext_common('backend', backend_data)
        return backend.work_root(task_id)

    def submit(self, backend_data, task_id, sub_ids, launcher_exe):
        backend = self.__ext_mgr.load_ext_common('backend', backend_data)
        return backend.submit(task_id, sub_ids, launcher_exe)
