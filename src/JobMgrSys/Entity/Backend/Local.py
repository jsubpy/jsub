from subprocess import Popen

from ...Core.Backend import Backend

class Local(Backend):
    def submit(self, param):
        script = param['script']

        submit_ok = True
        try:
            process = Popen([script])
        except OSError, x:
            print 'Can not create process: %s' % x
            submit_ok = False

        status = {}
        status['submit'] = submit_ok
        if submit_ok:
            status['pid'] = process.pid

        return status
