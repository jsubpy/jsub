import click

from jsub import Jsub

class Package(object):
    def __init__(self, config_user):
        self.__config_user = config_user

    def execute(self):
        click.echo('Package...')

        j = Jsub(self.__config_user)
        for pack in j.package():
            click.echo(pack)
