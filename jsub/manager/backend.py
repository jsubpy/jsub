class BackendManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def property(self, backend_data):
        backend = self.__ext_mgr.load_ext_common('backend', backend_data)
        return backend.property()

    def clean_work_dir(self, backend_data, task_id):
        backend = self.__ext_mgr.load_ext_common('backend', backend_data)
        return backend.clean_work_dir(task_id)

    def main_work_dir(self, backend_data, task_id):
        backend = self.__ext_mgr.load_ext_common('backend', backend_data)
        return backend.main_work_dir(task_id)

    def create_launcher(self, backend_data, task_id):
        backend = self.__ext_mgr.load_ext_common('backend', backend_data)
        return backend.create_launcher(task_id)

    def submit(self, backend_data, task_id, sub_ids):
        backend = self.__ext_mgr.load_ext_common('backend', backend_data)
        return backend.submit(task_id, sub_ids)
