import click

from jsub import Jsub

from jsub.config  import load_config_file

class Create(object):
    def __init__(self, jsubrc, task_profile_file):
        self.__jsubrc = jsubrc
        self.__task_profile_file = task_profile_file

    def execute(self):
        click.echo('Creating')

        j = Jsub(self.__jsubrc)
        task_profile = load_config_file(self.__task_profile_file)
        task = j.create(task_profile)

        click.echo('Task %s created: %s' % (task.data['task_id'], task.data['name']))
