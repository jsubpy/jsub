from jsub.config        import load_config_file

from jsub.manager.error import BackendNotSetupError

class ConfigManager(object):
    default_settings = {
        'log_level': 'INFO',
        'work_dir': '~/jsub/work',
        'max_cycle': 10000,
    }

    def __init__(self, jsubrc):
        self.__config = load_config_file(jsubrc)

    def extensions(self):
        return ['jsub.exts']

    def setting(self, item):
        if item in self.__config:
            return self.__config[item]
        if item in default_settings:
            return default_settings[item]
        raise ConfigNotSetupError('Configuration not found for: %s' % item)

    def repo(self):
        if 'repo' in self.__config:
            return self.__config['repo']
        config_repo = {}
        config_repo['type'] = 'file_system'
        config_repo['param'] = {'dir': '~/jsub/repo', 'format': 'compact'}
        return config_repo

    def content(self):
        if 'content' in self.__config:
            return self.__config['content']
        config_content = {}
        config_content['type'] = 'file_system'
        config_content['param'] = {'dir': '~/jsub/repo'}
        return config_content

    def bootstrap(self):
        if 'bootstrap' in self.__config:
            return self.__config['bootstrap']
        return 'shell'

    def navigator(self):
        if 'navigator' in self.__config:
            return self.__config['navigator']
        return ['python']


    def task_name(self, task_profile):
        if 'name' in task_profile:
            return task_profile['name']
        return task_profile['app']


    def app_data(self, task_profile):
        app_type = task_profile.get('app', 'common')
        app_param = task_profile.get('param', {})
        return {'type': app_type, 'param': app_param}


    def backend_data(self, task_profile):
        if 'backend' not in task_profile:
            try:
                backend_name = self.__config['backend']
            except KeyError:
                raise BackendNotSetupError('Must specify a backend')
        else:
            backend_in_profile = task_profile['backend']
            if isinstance(backend_in_profile, str):
                backend_name = backend_in_profile
#            elif isinstance(backend_in_profile, dict):
#                if 'type' not in backend_value:
#                    raise BackendNotSetupError('Must specify the backend type')
#                backend_type = backend_value['type']
#                backend_param_profile = backend_value['param']
            else:
                raise BackendNotSetupError('Backend value format not correct')

        backend_type = self.__config.get('backends', {}).get(backend_name, {}).get('type')
        backend_param = self.__config.get('backends', {}).get(backend_name, {}).get('param')
#        backend_param.update(backend_param_profile)

        backend_param['default_work_dir'] = self.__config.get('work_dir', '~/jsub/work')

        return {'type': backend_type, 'param': backend_param}
