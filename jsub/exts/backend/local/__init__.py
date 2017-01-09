run_on = 'local'
run_on = 'remote'

run_on_background = True

# could be used for tests
run_on_foregroud = True

import os
import time
import subprocess

CLOCK_TICKS = os.sysconf('SC_CLK_TCK')

from jsub.util import safe_mkdir

from jsub.mixin.backend.common import Common

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
        self.initialize_common_param()
        self._foreground = param.get('foreground', False)
        self._max_submit = param.get('max_submit', 4)

    def property(self):
        return {}

    def submit(self, task_id, sub_ids):
        processes = {}

        count = 0
        for sub_id in sub_ids:
            if count >= self._max_submit:
                break

            try:
                process = self.__submit_job(task_id, sub_id)
                start_time = _process_start_time(process.pid)
            except OSError as e:
                # warning('Submit job (%s.%s) to local failed: %s' % (task_id, sub_id, e))
                continue

            count += 1
            processes[sub_id] = {}
            processes[sub_id]['process'] = process
            processes[sub_id]['start_time'] = start_time

        if self._foreground:
            for sub_id, data in processes.items():
                data['process'].wait()

        result = {}
        for sub_id, data in processes.items():
            result[sub_id] = '%s_%s' % (data['start_time'], data['process'].pid)
        return result

    def __submit_job(self, task_id, sub_id):
        sub_log_dir = os.path.join(self.launcher_log_dir(task_id), str(sub_id))
        safe_mkdir(sub_log_dir)
        fout = open(os.path.join(sub_log_dir, 'launcher.out'), 'w')
        ferr = open(os.path.join(sub_log_dir, 'launcher.err'), 'w')

        launcher = self.launcher_work_path(task_id)

        return subprocess.Popen([launcher, str(sub_id)], stdout=fout, stderr=ferr)
