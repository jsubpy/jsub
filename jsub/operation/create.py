from jsub.operation.exception import AppNotSetupError, SplitterNotSetupError

from jsub.task import TaskPool

class Create(object):
    def __init__(self, task_profile, loader, task_pool, content):
        self.__task_profile = task_profile
        self.__loader       = loader
        self.__task_pool    = task_pool
        self.__content      = content

    def handle(self):
        app = self.__load_app()

        app_data = app.build()

        app_input = app_data.get('input',    {})
        workflow  = app_data.get('workflow', {})
        prop      = app_data.get('prop',     {})
        splitter  = app_data.get('splitter', {})

        all_jobvar = self.__split(splitter)
        all_app_input = list(app_input.keys())

        task_id = self.__create_task(workflow, prop, all_jobvar, all_app_input)

        self.__copy_input_file(task_id, app_input)

        return task_id


    def __load_app(self):
        if 'app' not in self.__task_profile:
            raise AppNotSetupError('Must setup an app in task profile')

        app_type   = self.__task_profile['app']
        app_param = self.__task_profile.get('param', {})

        return self.__loader.load('app', {'type': app_type, 'param': app_param})

    def __jobvar_name_map(self, jobvar_single, name_map):
        jobvar_new = {}
        for k, v in jobvar_single.items():
            if k in name_map:
                jobvar_new[name_map[k]] = v
            else:
                jobvar_new[k] = v
        return jobvar_new

    def __split(self, all_splitter):
        splitter_content = {}
        for splitter, value in all_splitter.items():
            if 'type' not in value:
                raise SplitterNotSetupError('Splitter type not setup: %s', splitter)

            splitter_content[splitter] = {}
            splitter_content[splitter]['instance'] = self.__loader.load('splitter', value)
            splitter_content[splitter]['name_map'] = value.get('name_map', {})

        all_jobvar = []
        split_finished = False
        while True:
            jobvar = {}
            try:
                for splitter, content in splitter_content.items():
                    jobvar_single = content['instance'].next()
                    jobvar.update(self.__jobvar_name_map(jobvar_single, content['name_map']))
            except StopIteration:
                break
            all_jobvar.append(jobvar)

        return all_jobvar

    def __create_task(self, workflow, prop, all_jobvar, all_app_input):
        task = self.__task_pool.create(workflow, prop, all_jobvar, all_app_input)
        return task.data['task_id']

    def __copy_input_file(self, task_id, app_input):
        for dst, src in app_input.items():
            self.__content.put(task_id, 'input', src, dst)
