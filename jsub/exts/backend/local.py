import os
import time
import subprocess
import logging

from jsub.mixin.backend.common import Common


CLOCK_TICKS = os.sysconf('SC_CLK_TCK')

def _process_start_time(pid):
	start_time = 0
	try:
		with open('/proc/%s/stat' % pid, 'r') as f:
			start_time = int(f.read().split()[21]) // CLOCK_TICKS
	except IOError:
		# warning('PID not found: %s' % pid)
		return int(time.time())

	boot_time = 0
	with open('/proc/stat', 'r') as f:
		for line in f:
			if line.startswith('btime'):
				boot_time = int(line.strip().split()[1])
				break

	return boot_time + start_time


class Local(Common):
	def __init__(self, param):
		self._param = param

		self._logger = logging.getLogger('JSUB')

		self._foreground = param.get('foreground', False)
		self._max_submit = param.get('max_submit', 4)
		self._max_submit = param.get('maxSubmit', self._max_submit)

		self.initialize_common_param()

	def property(self):
		return {'run_on': 'local', 'name': 'local'}

	def get_log(self, task_data = None, path = './', sub_ids = [], status = [], njobs = 10):
		task_id = task_data.get('id')
		getlog_result={}
		if status:
			print('Cannot filter subjobs with status on local backend, please filter sub_ids instead.')
		for sid in sub_ids:
			try:
				#cp logfiles from runtime folder to log folder
				source_folder = os.path.join(self.get_run_root(task_id),'subjobs',str(sid),'log')
				destination_folder = os.path.join(self.get_task_root(task_id),'logfiles',str(sid))
				os.system('mkdir -p %s >/dev/null 2>/dev/null'%destination_folder)
				os.system('mv %s/* %s >/dev/null 2>/dev/null'%(source_folder,destination_folder))
				getlog_result.update({sid:{'OK':True,'Message':''}})
			except:
				self._logger.error('Failed to get log files of subjob %s' % (sid))
				getlog_result.update({sid:{'OK':False,'Message':'Failed to copy logfiles to location.'}})
				continue
		return getlog_result

	def submit(self, task_id, launcher_param,  sub_ids=None):
		launcher_exe = launcher_param['executable']

		processes = {}

		count = 0
		for sub_id in sub_ids:
			if count >= self._max_submit:
				print("Exceeding max submit on local backend. (%d subjobs)"%self._max_submit)
				

			try:
				launcher = os.path.join(self.get_run_root(task_id), launcher_exe)

				FNULL = open(os.devnull, 'w')
				process = subprocess.Popen([launcher, str(sub_id)], stdout=FNULL, stderr=subprocess.STDOUT)
				start_time = _process_start_time(process.pid)
			except OSError as e:
				self._logger.error('Submit job (%s.%s) to "local" failed: %s' % (task_id, sub_id, e))
				continue

			count += 1
			processes[sub_id] = {}
			processes[sub_id]['process'] = process
			processes[sub_id]['start_time'] = start_time

		if self._foreground:
			for _, data in processes.items():
				data['process'].wait()

		result = {}
		for sub_id, data in processes.items():
			result[sub_id] = '%s_%s' % (data['start_time'], data['process'].pid)
		return result
