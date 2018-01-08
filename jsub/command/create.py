import click

from jsub import Jsub

from jsub.config  import load_config_file

class Create(object):
    def __init__(self, config_user, task_profile_file):
        self.__config_user = config_user
        self.__task_profile_file = task_profile_file

    def execute(self):
        j = Jsub(self.__config_user)
        task_profile = load_config_file(self.__task_profile_file)
        task = j.create(task_profile)

        click.echo('Task created successfully')
        click.echo('- ID         : %s' % task.data['id'])
        click.echo('- Name       : %s' % task.data['name'])
        click.echo('- Job Number : %s' % len(task.data['jobvar']))
