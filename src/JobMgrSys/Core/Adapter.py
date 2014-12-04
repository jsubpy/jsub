from .Entity import Entity

class Adapter(Entity):
    def commonAdapt(self, common_param, repository):
        raise Exception('not implemented')

    def subAdapt(self, job_id, common_param, sub_param, repository):
        raise Exception('not implemented')
