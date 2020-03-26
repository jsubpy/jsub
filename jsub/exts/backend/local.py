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

		self.initialize_common_param()

	def property(self):
		return {'run_on': 'local'}

	def submit(self, task_id, sub_ids, launcher_param):
		launcher_exe = launcher_param['executable']

		processes = {}

		count = 0
		for sub_id in sub_ids:
			if count >= self._max_submit:
				print("Exceeding max submit (%d subjobs)"%self._max_submit)
				break

			try:
				launcher = os.path.join(self.get_work_root(task_id), launcher_exe)

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
