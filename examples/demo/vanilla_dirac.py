import DIRAC
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Interfaces.API.Dirac import Dirac

def submitWMS():
	job = Job()
	dirac = Dirac()
	job.setName('HelloJuno')
	job.setExecutable('./HelloJuno.sh')
	job.setInputSandbox(['HelloJuno.sh','input.file'])
	job.setOutputSandbox(['output.file'])
	result = dirac.submitJob(job)




