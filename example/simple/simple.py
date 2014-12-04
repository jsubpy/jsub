import SimpleJob

from JobMgrSys.Entity.Application.SingleCommand import SingleCommand
from JobMgrSys.Entity.Splitter.FileLineSplitter import FileLineSplitter
from JobMgrSys.Entity.Backend.Local import Local
from JobMgrSys.Entity.Backend.Pbs import Pbs
from JobMgrSys.Entity.Backend.Dirac import Dirac

j = Job()

app = SingleCommand()
app.setCommand('script')
#app.setArgs(['bing.com'])
j.setApplications([app])

splitter = FileLineSplitter('web')
j.setSplitter(splitter)

backend = Local()

#backend = Pbs()
#backend.setQueue('midq')

#backend = Dirac()
#backend.setSite('CLUSTER.UCAS.cn')

j.setBackend(backend)

j.prepare()

j.submit()
