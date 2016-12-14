from jsub.config.config_loader import load_default
from jsub.loader import Loader
from jsub.task import TaskPool

from jsub.operation.create import Create
from jsub.operation.submit import Submit

from jsub.operation.exception import RepositoryNotSetupError
from jsub.operation.exception import ContentNotSetupError

class Operation(object):
    def __init__(self):
        self.__default_config = load_default()
        self.__loader = Loader(['jsub.exts'])

        self.__load_extensions()
        self.__load_extension_config()

        self.__load_task_pool()
        self.__load_content()

    def __load_extensions(self):
        # recursive problems
        pass

    def __load_extension_config(self):
        # recursive problems
        self.__config = self.__default_config.copy()

    def __load_task_pool(self):
        if 'repo' not in self.__config:
            raise RepositoryNotSetupError('Repository is not setup in the configuration')
        repo = self.__loader.load('repo', self.__config['repo'])
        self.__task_pool = TaskPool(repo)

    def __load_content(self):
        if 'content' not in self.__config:
            raise ContentNotSetupError('Content is not setup in the configuration')
        self.__content = self.__loader.load('content', self.__config['content'])


    def create(self, task_profile):
        handler = Create(task_profile, self.__loader, self.__task_pool, self.__content)
        return handler.handle()

    def submit(self, task_id, task_sub_id=None, dry_run=False):
        handler = Submit(task_id, self.__repo, self.__loader)
        return handler.handle()
