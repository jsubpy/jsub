import os
import json

from ...Core.Repository import Repository
from ...Core import gSysParam

class CwdRepository(Repository):
    repo_main_dir = 'repo'

    def __init__(self):
        self.__cwd = gSysParam['script']['dir']
        self.__getRepoDir()

    def __validateDir(self, dir):
        if not os.path.isdir(dir):
            os.makedirs(dir)

    def __getRepoDir(self):
        repo_id = 0
        while True:
            repo_dir = os.path.join(self.__cwd, self.__class__.repo_main_dir, '%d'%repo_id)
            if not os.path.lexists(repo_dir):
                break
            repo_id += 1
        self.__repo_id = repo_id
        self.__repo_dir = repo_dir
        os.makedirs(repo_dir)

    def getRepoId(self):
        return self.__repo_id

    def getJobInputDir(self):
        input_dir = os.path.join(self.__repo_dir, 'job', 'input')
        self.__validateDir(input_dir)
        return input_dir

    def getJobOutputDir(self):
        output_dir = os.path.join(self.__repo_dir, 'job', 'output')
        self.__validateDir(output_dir)
        return output_dir

    def getSubJobInputDir(self, number):
        input_dir = os.path.join(self.__repo_dir, 'subjob', '%d'%number, 'input')
        self.__validateDir(input_dir)
        return input_dir

    def getSubJobOutputDir(self, number):
        output_dir = os.path.join(self.__repo_dir, 'subjob', '%d'%number, 'output')
        self.__validateDir(output_dir)
        return output_dir


    def getJobParamDir(self):
        param_dir = os.path.join(self.__repo_dir, 'params')
        self.__validateDir(param_dir)
        return param_dir

    def getJobStatusDir(self):
        status_dir = os.path.join(self.__repo_dir, 'status')
        self.__validateDir(status_dir)
        return status_dir


    def __saveData(self, data, data_path):
        json_str = json.dumps(data, indent=2, sort_keys=True)
        f = open(data_path, 'w')
        f.write(json_str)
        f.close()

    def saveAppParam(self, app_param):
        param_dir = self.getJobParamDir()
        app_param_path = os.path.join(param_dir, 'app')
        self.__saveData(app_param, app_param_path)

    def saveJobParam(self, job_param):
        param_dir = self.getJobParamDir()
        job_param_path = os.path.join(param_dir, 'job')
        self.__saveData(job_param, job_param_path)

    def saveBackendParam(self, backend_param):
        param_dir = self.getJobParamDir()
        backend_param_path = os.path.join(param_dir, 'backend')
        self.__saveData(backend_param, backend_param_path)

    def saveJobStatus(self, number, status):
        status_dir = self.getJobStatusDir()
        job_status_path = os.path.join(status_dir, 'job_%d'%number)
        self.__saveData(status, job_status_path)
