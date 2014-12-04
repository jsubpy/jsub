import os
import shutil
import copy

from ...Core.Adapter import Adapter

class SingleCommandRemoteAdapter(Adapter):
    def __init__(self):
        self.__common_backend_param = {}

    def commonAdapt(self, app_param, repository):
        command = app_param[0]['command']
        command_basename = os.path.basename(command)
        shutil.copy(command, repository.getJobInputDir())
        command_path = os.path.join(repository.getJobInputDir(), os.path.basename(app_param[0]['command']))

        repo_id = repository.getRepoId()

        self.__common_backend_param['repo_id'] = repo_id
        self.__common_backend_param['command'] = command_basename
        self.__common_backend_param['command_path'] = command_path
        self.__common_backend_param['input'] = [command_path]
        self.__common_backend_param['output'] = ['script.out', 'script.err']

    def subAdapt(self, job_id, app_param, sub_job_param, repository):
        backend_param = copy.deepcopy(self.__common_backend_param)

        script_path = os.path.join(repository.getSubJobInputDir(job_id), 'run.sh')
        output_dir = repository.getSubJobOutputDir(job_id)

        self.__createScript(script_path, output_dir, backend_param['command'], sub_job_param['args'])

        backend_param['job_name'] = 'JMS_%s_%d.%d' % (app_param[0]['name'], backend_param['repo_id'], job_id)
        backend_param['script'] = script_path
        backend_param['output_dir'] = output_dir
        return backend_param

    def __createScript(self, script_path, output_dir, command, args):
        script = """#!/bin/bash

./%s %s 1>script.out 2>script.err
""" % (command, ' '.join(args))

        f = open(script_path, 'w')
        f.write(script)
        f.close()

        os.chmod(script_path, 0755)
