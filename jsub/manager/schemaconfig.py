import pytz

from schema import Schema, And, Or, Use, Optional, Regex

from jsub.util import ensure_list


_timezone_map = {tz.lower(): tz for tz in pytz.all_timezones}

_config_schema = {
    Optional('log_level', default='INFO'): And(str, Use(str.upper),
                                               lambda s: s in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')),
    Optional('time_zone', default='UTC'): And(str, Use(str.lower), lambda s: s in _timezone_map, Use(lambda s: _timezone_map[s])),
    Optional('package'): And(Or(str, [str]), Use(lambda f: ['jsub.exts'] + ensure_list(f))),
}

_task_profile_schema = {
}


class SchemaManager(object):
    def __init__(self):
        pass

    def validate_jsubrc_config(self, config):
        return config

    def validate_package_config(self, config):
        return config

    def validate_final_config(self, config):
        return config

    def validate_task_profile(self, task_profile):
        return task_profile
