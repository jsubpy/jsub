import click

from jsub import Jsub
import logging

class Submit(object):
    def __init__(self, jsubrc, task_id, dry_run,resubmit):
        self.__jsubrc = jsubrc
        self.__task_id = task_id
        self.__dry_run = dry_run
        self.__resubmit = resubmit

    def execute(self):
        click.echo('Submitting task %d'%self.__task_id)
		

        j = Jsub(self.__jsubrc)
        j.submit(self.__task_id, dry_run=self.__dry_run, resubmit=self.__resubmit)
