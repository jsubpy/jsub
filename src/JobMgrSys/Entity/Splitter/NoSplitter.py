from ...Core.Splitter import Splitter

class NoSplitter(Splitter):
    def split(self, app_params):
        job_params = []
        one_job = {}
        one_job['args'] = app_params[0]['args']
        job_params.append(one_job)
        return job_params
