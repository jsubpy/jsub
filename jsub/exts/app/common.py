class Common(object):
    def __init__(self, task_name, app_config):
        self.__task_name = task_name
        self.__app_param = app_param

    def initialize(self):
        pass

    def task_props(self):
        props = {}
        return props

    def main_splitter(self):
        return self.__app_param['splitter']:

    def generate_final(self, backend=None):
        dag = DAG()
        for module in self.__app_param['module']:
            pass
        return dag

    def generate_modvar(self):
        pass

    def generate_jobvar(self):
        pass

    def generate_module(self):
        pass

    def generate(self):
        self.generate_workflow()
        for splitter in all_splitter:
            self.generate_jobvar()

        common_input()
        for unit in units:
            unit_input(unit)

    def get_workflow(self):
        pass

    def get_unit_module(self):
        pass

    def get_unit_modvars(self):
        pass

    def get_input(self):
        pass

    def get_unit_input(self):
        pass

    def get_splitters(self):
        pass
