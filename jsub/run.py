#!/usr/bin/env python

import click

from jsub.config.config_loader import load_default, load_and_merge

@click.group()
def cli():
    pass

@cli.command()
@click.option('--submit', help='Submit to backend after creation')
@click.argument('config_file')
def create(submit, config_file):
    click.echo('Creating')
    click.echo('Submit to: %s' % submit)
    final_config = load_and_merge(config_file)
#    t = Task(final_config)
#    t.create()

@cli.command()
@click.argument('task_id')
def submit(task_id):
    click.echo('Submitting')
    t = Task.load(task_id)
    t.submit()

@cli.command()
@click.argument('task_id')
def status(task_id):
    click.echo('Status')
    j = Job.load()

def main():
    load_default()
    cli()

if __name__ == '__main__':
    main()
