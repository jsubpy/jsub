from jsub.manager.error import SequencerNotSetupError
#translate jobvar_single (from sequencer extension) according to name_map (from task profile)
def _jobvar_name_map(jobvar_single, name_map):
    jobvar_new = {}
    for k, v in jobvar_single.items():
        if k in name_map:
            jobvar_new[name_map[k]] = v
        else:
            jobvar_new[k] = v
    return jobvar_new


class SequencerManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def sequence(self, sequencers, max_cycle=100000):
        jobvars = []

        if not sequencers:
            return jobvars

        sequencer_content = {}
        for sequencer, value in sequencers.items():
            if 'type' not in value:
                raise SequencerNotSetupError('Sequencer type not setup: %s', sequencer)

            sequencer_content[sequencer] = {}
            sequencer_content[sequencer]['instance'] = self.__ext_mgr.load_ext_common('sequencer', value)
            sequencer_content[sequencer]['name_map'] = value.get('name_map', {})

        cycle = 0
        while cycle < max_cycle:
            cycle += 1

            jobvar = {}
            try:
                for sequencer, content in sequencer_content.items():
                    jobvar_single = content['instance'].next() 
                    jobvar.update(_jobvar_name_map(jobvar_single, content['name_map']))
            except StopIteration:
                break
            jobvars.append(jobvar)

        return jobvars
