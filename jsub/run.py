#!/usr/bin/env python

import click

import jsub

from jsub.config.config_loader import load_config

@click.group()
def cli():
    pass


@cli.command()
def version():
    click.echo('JSUB (Job Submission Utility Bundle) version %s' % jsub.version())


@cli.command()
@click.option('--backend', help='Backend to submit')
@click.argument('task_profile_file')
def create(submit, task_profile_file):
    click.echo('Creating')
    click.echo('Submit to: %s' % submit)

    task_profile = load_config(task_profile_file)
    task_id = jsub.create(task_profile)

    click.echo('Task %s created' % task_id)


@cli.command()
@click.argument('task_id')
def submit(task_id):
    click.echo('Submitting')
    jsub.submit(task_id)


@cli.command()
@click.argument('task_id')
def show(task_id):
    click.echo('Show')
    jsub.submit(task_id)


def main():
    cli()

if __name__ == '__main__':
    main()
