from ...Core.Splitter import Splitter

class FileLineSplitter(Splitter):
    def __init__(self, line_file=''):
        self.__line_file = line_file

    def split(self, app_params):
        job_params = []

        f = open(self.__line_file)
        for line in f:
            one_job = {}
            one_job['args'] = app_params[0]['args'] + line.split()
            job_params.append(one_job)
        f.close()

        return job_params

    def setLineFile(self, line_file):
        self.__line_file = line_file
