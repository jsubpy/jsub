#!/usr/bin/env python

import click

from jsub import version as jsub_version

from jsub.command.create  import Create
from jsub.command.submit  import Submit
from jsub.command.run     import Run
from jsub.command.show    import Show


@click.group()
@click.option('--jsubrc', default='~/.jsubrc', help='Path for jsubrc default configuration file')
@click.pass_context
def cli(ctx, jsubrc):
    ctx.obj['jsubrc'] = jsubrc


@cli.command()
def version():
    click.echo('JSUB (Job Submission Utility Bundle) version %s' % jsub_version())


@cli.command()
@click.argument('task_profile')
@click.pass_context
def create(ctx, task_profile):
    cmd = Create(jsubrc=ctx.obj['jsubrc'], task_profile_file=task_profile)
    cmd.execute()


@cli.command()
@click.option('--dry-run', is_flag=True, help='Create necessary files without final submission')
@click.argument('task_id', type=int)
@click.pass_context
def submit(ctx, dry_run, task_id):
    cmd = Submit(jsubrc=ctx.obj['jsubrc'], task_id=task_id, dry_run=dry_run)
    cmd.execute()


@cli.command()
@click.option('--dry-run', is_flag=True, help='Create necessary files without final submission')
@click.argument('task_profile')
@click.pass_context
def run(ctx, dry_run, task_profile):
    cmd = Run(jsubrc=ctx.obj['jsubrc'], task_profile_file=task_profile, dry_run=dry_run)
    cmd.execute()


@cli.command()
@click.argument('task_id', type=int)
@click.pass_context
def show(ctx, task_id):
    cmd = Show(jsubrc=ctx.obj['jsubrc'], task_id=task_id)
    cmd.execute()


def main():
    cli(obj={})

if __name__ == '__main__':
    main()
