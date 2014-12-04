from subprocess import Popen, PIPE

from ...Core.Backend import Backend

class Pbs(Backend):
    def __init__(self, queue=''):
        self.__queue = queue

    def submit(self, param):
        job_name = param['job_name']
        script = param['script']
        output_dir = param['output_dir']

        qsub_cmd = ['qsub', '-j', 'oe', '-o', '/dev/null']
        if self.__queue:
            qsub_cmd += ['-q', self.__queue]
        qsub_cmd += ['-N', job_name]
        qsub_cmd += [script]
        process = Popen(qsub_cmd, stdout=PIPE)
        exit_code = process.wait()
        job_id = process.stdout.read().rstrip()

        status = {}
        status['submit'] = (exit_code==0)
        if status['submit']:
            status['job_id'] = job_id

        return status

    def setQueue(self, queue):
        self.__queue = queue
