def _jobvar_name_map(jobvar_single, name_map):
    jobvar_new = {}
    for k, v in jobvar_single.items():
        if k in name_map:
            jobvar_new[name_map[k]] = v
        else:
            jobvar_new[k] = v
    return jobvar_new


class SplitterManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def split(self, splitters, max_cycle=100000):
        splitter_content = {}
        for splitter, value in splitters.items():
            if 'type' not in value:
                raise SplitterNotSetupError('Splitter type not setup: %s', splitter)

            splitter_content[splitter] = {}
            splitter_content[splitter]['instance'] = self.__ext_mgr.load_ext_common('splitter', value)
            splitter_content[splitter]['name_map'] = value.get('name_map', {})

        jobvars = []
        cycle = 0
        while cycle < max_cycle:
            cycle += 1

            jobvar = {}
            try:
                for splitter, content in splitter_content.items():
                    jobvar_single = content['instance'].next()
                    jobvar.update(_jobvar_name_map(jobvar_single, content['name_map']))
            except StopIteration:
                break
            jobvars.append(jobvar)

        return jobvars
