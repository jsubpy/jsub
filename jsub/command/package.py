import click

from jsub import Jsub

class Package(object):
    def __init__(self, jsubrc):
        self.__jsubrc = jsubrc

    def execute(self):
        click.echo('Current active packages:')

        j = Jsub(self.__jsubrc)
        for pack in j.package():
            click.echo(pack)
