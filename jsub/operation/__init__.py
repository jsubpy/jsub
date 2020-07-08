class Operation(object):
	def __init__(self, manager):
		self.__manager = manager


	def rename(self, task, new_name):
		from jsub.operation.rename import Rename
		return Rename(self.__manager, task, new_name).handle()

	def create(self, task_profile):
		from jsub.operation.create import Create
		return Create(self.__manager, task_profile).handle()

	def submit(self, task, sub_ids=None, dry_run=False, resubmit=False):
		from jsub.operation.submit import Submit
		return Submit(self.__manager, task, sub_ids, dry_run, resubmit).handle()

	def remove(self, task, force):
		from jsub.operation.remove import Remove
		return Remove(self.__manager, task, force).handle()

	def status(self, task_id, states=None, silent=False):
		from jsub.operation.status import Status
		return Status(self.__manager, task_id, states, silent).handle()

	def getlog(self, task_id, sub_id, path):
		from jsub.operation.getlog import Getlog
		return Getlog(self.__manager, task_id, sub_id = sub_id, path = path).handle()

	def ls(self, task_id, update):
		from jsub.operation.ls import Ls
		return Ls(self.__manager, task_id, update).handle()

	def show(self, task_id, dump):
		from jsub.operation.show import Show
		return Show(self.__manager, task_id, dump).handle()

	def reschedule(self, task_id, status, sub_id, backend_id):
		from jsub.operation.reschedule import Reschedule
		return Reschedule(self.__manager, task_id, status, sub_id, backend_id).handle()
