import os

from jsub.config import dump_config_string

class Create(object):
    def __init__(self, manager, task_profile):
        self.__manager      = manager
        self.__task_profile = task_profile

        self.__initialize_manager()

    def __initialize_manager(self):
        self.__config_mgr   = self.__manager.load_config_manager()

        self.__app_mgr      = self.__manager.load_app_manager()
        self.__splitter_mgr = self.__manager.load_splitter_manager()
        self.__backend_mgr  = self.__manager.load_backend_manager()


    def handle(self):
        task_name = self.__config_mgr.task_name(self.__task_profile)

        backend_data = self.__config_mgr.backend_data(self.__task_profile)
        backend_property = self.__backend_mgr.property(backend_data)

        app_data = self.__config_mgr.app_data(self.__task_profile)
        app_result = self.__app_mgr.build(app_data, backend_property)

        app_input = app_result.get('input',    {})
        workflow  = app_result.get('workflow', {})
        prop      = app_result.get('prop',     {})
        splitter  = app_result.get('splitter', {})

        jobvar = self.__splitter_mgr.split(splitter)

        task_data = {}
        task_data['name']       = task_name
        task_data['app']        = app_data
        task_data['workflow']   = workflow
        task_data['event']      = {}
        task_data['prop']       = prop
        task_data['splitter']   = splitter
        task_data['jobvar']     = jobvar
        task_data['input_file'] = list(app_input.keys())
        task_data['backend']    = backend_data
        task_data['status']     = 'NEW'
        task = self.__create_task(task_data)
        task_id = task.data['task_id']

        self.__copy_input_file(task_id, app_input)
        self.__dump_task_profile(task_id)

        return task


    def __create_task(self, task_data):
        task_pool = self.__manager.load_task_pool()
        return task_pool.create(task_data)

    def __copy_input_file(self, task_id, app_input):
        content = self.__manager.load_content()

        if 'common' in app_input:
            for dst, src in app_input['common'].items():
                content.put(task_id, src, os.path.join('input', 'common', dst))

        if 'unit' in app_input:
            for unit, unit_file_pair in app_input['unit'].items():
                for dst, src in unit_file_pair.items():
                    content.put(task_id, src, os.path.join('input', 'unit', unit, dst))

    def __dump_task_profile(self, task_id):
        content = self.__manager.load_content()
        content.put_str(task_id, dump_config_string(self.__task_profile, 'yaml'), os.path.join('profile', 'origin'))
