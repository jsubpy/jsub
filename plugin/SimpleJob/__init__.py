from JobMgrSys.Core.Job import Job

from JobMgrSys.Entity.Repository.CwdRepository import CwdRepository

#from JobMgrSys.Entity.Application.SingleCommand import SingleCommand
from JobMgrSys.Entity.Adapter.SingleCommandLocalAdapter import SingleCommandLocalAdapter
from JobMgrSys.Entity.Adapter.SingleCommandRemoteAdapter import SingleCommandRemoteAdapter
#from JobMgrSys.Entity.Backend.Local import Local
#from JobMgrSys.Entity.Backend.Pbs import Pbs
#from JobMgrSys.Entity.Backend.Dirac import Dirac
from JobMgrSys.Entity.Splitter.NoSplitter import NoSplitter

j = Job()
j.initialize()

j.setRepository(CwdRepository())
j.setDefaultSplitter(NoSplitter())

j.setAdapterMap('Local', SingleCommandLocalAdapter())
j.setAdapterMap('Pbs', SingleCommandLocalAdapter())
j.setAdapterMap('Dirac', SingleCommandRemoteAdapter())
