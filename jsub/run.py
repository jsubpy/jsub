#!/usr/bin/env python

import click

from jsub import Jsub

from jsub.config import load_config_file

@click.group()
@click.option('--jsubrc', default='~/.jsubrc', help='Path for jsubrc default configuration file')
@click.pass_context
def cli(ctx, jsubrc):
    ctx.obj['jsubrc'] = jsubrc


@cli.command()
def version():
    click.echo('JSUB (Job Submission Utility Bundle) version %s' % Jsub().version())


@cli.command()
@click.argument('task_profile_file')
@click.pass_context
def create(ctx, task_profile_file):
    click.echo('Creating')

    j = Jsub(ctx.obj['jsubrc'])
    task_profile = load_config_file(task_profile_file)
    task = j.create(task_profile)

    click.echo('Task %s created: %s' % (task.data['task_id'], task.data['name']))


@cli.command()
@click.option('--dry-run', is_flag=True, help='Create necessary files without final submission')
@click.argument('task_id')
@click.pass_context
def submit(ctx, dry_run, task_id):
    click.echo('Submitting')

    j = Jsub(ctx.obj['jsubrc'])
    j.submit(task_id, dry_run=dry_run)


@cli.command()
@click.option('--dry-run', is_flag=True, help='Create necessary files without final submission')
@click.argument('task_profile_file')
@click.pass_context
def run(ctx, dry_run, task_profile_file):
    click.echo('Running')

    j = Jsub(ctx.obj['jsubrc'])
    task_profile = load_config_file(task_profile_file)
    task = j.create(task_profile)
    j.submit(task, dry_run=dry_run)

    click.echo('Task %s submitted: %s' % (task.data['task_id'], task.data['name']))


@cli.command()
@click.argument('task_id')
@click.pass_context
def show(ctx, task_id):
    click.echo('Show')
    j = Jsub(ctx.obj['jsubrc'])
    j.show(task_id)


def main():
    cli(obj={})

if __name__ == '__main__':
    main()
