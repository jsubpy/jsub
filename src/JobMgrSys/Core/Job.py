class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class Job(Singleton):
    def __init__(self):
        pass

    def initialize(self):
        self.__applications = []
        self.__splitter = None
        self.__default_splitter = None
        self.__backend = None
        self.__repository = None
        self.__all_adapters = {}

    def setApplications(self, applications):
        self.__applications = applications

    def setDefaultSplitter(self, splitter):
        self.__default_splitter = splitter

    def setSplitter(self, splitter):
        self.__splitter = splitter

    def setBackend(self, backend):
        self.__backend = backend

    def setRepository(self, repository):
        self.__repository = repository

    def setAdapterMap(self, backend_name, adapter):
        self.__all_adapters[backend_name] = adapter


    def prepare(self):
        self.__app_params = self.__appInit()
        self.__repository.saveAppParam(self.__app_params)

        self.__job_params = self.__split()
        self.__repository.saveJobParam(self.__job_params)

        self.__backend_params = self.__adapt()
        self.__repository.saveBackendParam(self.__backend_params)

    def submit(self):
        self.__submit()


    def __appInit(self):
        app_params = []
        for app in self.__applications:
            app.initialize()
            app_params.append(app.getParam())
        return app_params

    def __split(self):
        if self.__splitter is None:
            splitter = self.__default_splitter
        else:
            splitter = self.__splitter
        return splitter.split(self.__app_params)

    def __adapt(self):
        adapter = self.__all_adapters[self.__backend.getName()]

        adapter.commonAdapt(self.__app_params, self.__repository)

        repo_id = self.__repository.getRepoId()
        backend_params = []
        for job_id, sub_job_param in enumerate(self.__job_params):
            backend_param = adapter.subAdapt(job_id, self.__app_params, sub_job_param, self.__repository)
            backend_params.append(backend_param)
            print 'Job %d.%d created' % (repo_id, job_id)

        return backend_params

    def __submit(self):
        self.__backend.setEnv()
        repo_id = self.__repository.getRepoId()
        for job_id, backend_param in enumerate(self.__backend_params):
            status = self.__backend.submit(backend_param)
            self.__repository.saveJobStatus(job_id, status)
            if status['submit']:
                print 'Job %d.%d submitted' % (repo_id, job_id)
