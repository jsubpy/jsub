from ...Core.Backend import Backend

from DIRAC.Core.Base import Script
Script.initialize()

from DIRAC.Interfaces.API.Dirac import Dirac as GridDirac
from DIRAC.Interfaces.API.Job import Job

class Dirac(Backend):
    def __init__(self):
        self.__site = ''

    def submit(self, param):
        job_name = param['job_name']
        script = param['script']
        input = param['input']
        output = param['output']

        j = Job()
        j.setExecutable(script)
        if self.__site:
            j.setDestination(self.__site)
        j.setName(job_name)
        j.setInputSandbox(input)
        j.setOutputSandbox(output)
        if 'input_data' in param:
            j.setInputData(param['input_data'])

        dirac = GridDirac()
        result = dirac.submit(j)

        status = {}
        status['submit'] = result['OK']
        if status['submit']:
            status['job_id'] = result['Value']

        return status

    def setSite(self, site):
        self.__site = site
