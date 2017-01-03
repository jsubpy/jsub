run_on = 'local'
run_on = 'remote'

run_on_background = True

# could be used for tests
run_on_foregroud = True

import os

from jsub.mixin.backend.common import Common

class Local(Common):
    def __init__(self, param):
        self._param = param
        self.initialize_param()

    def property(self):
        return {}
