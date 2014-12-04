class Repository:
    def getRepoId(self):
        raise Exception('not implemented')

    def getJobInputDir(self):
        raise Exception('not implemented')

    def getJobOutputDir(self):
        raise Exception('not implemented')

    def getSubJobInputDir(self, number):
        raise Exception('not implemented')

    def getSubJobOutputDir(self, number):
        raise Exception('not implemented')

    def saveAppParam(self, app_param):
        raise Exception('not implemented')

    def saveJobParam(self, job_param):
        raise Exception('not implemented')

    def saveBackendParam(self, backend_param):
        raise Exception('not implemented')

    def saveJobStatus(self, number, status):
        raise Exception('not implemented')
