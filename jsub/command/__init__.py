import click


@click.group()
@click.option('--config', default='~/.jsub.conf', help='Path for jsub user configuration file')
@click.pass_context
def cli(ctx, config_user):
    ctx.obj['config_user'] = config_user


@cli.command()
def version():
    from jsub import version as jsub_version
    click.echo('JSUB (Job Submission Utility Bundle) version %s' % jsub_version())


@cli.command()
@click.argument('task_id', type=int)
@click.argument('new_name', type=str)
@click.pass_context
def rename(ctx, task_id, new_name):
    from jsub.command.rename import Rename
    cmd = Rename(config_user=ctx.obj['config_user'], task_id=task_id, new_name=new_name)
    cmd.execute()


@cli.command()
@click.argument('task_profile', type=click.Path(exists=True))
@click.pass_context
def create(ctx, task_profile):
    from jsub.command.create import Create
    task_profile_file = click.format_filename(task_profile)
    cmd = Create(config_user=ctx.obj['config_user'], task_profile_file=task_profile_file)
    cmd.execute()


@cli.command()
@click.option('--dry-run', is_flag=True, help='Create necessary files without final submission')
@click.argument('task_id', type=int)
@click.pass_context
def submit(ctx, dry_run, task_id):
    from jsub.command.submit import Submit
    cmd = Submit(config_user=ctx.obj['config_user'], task_id=task_id, dry_run=dry_run)
    cmd.execute()


@cli.command()
@click.option('--dry-run', is_flag=True, help='Create necessary files without final submission')
@click.argument('task_profile', type=click.Path(exists=True))
@click.pass_context
def run(ctx, dry_run, task_profile):
    from jsub.command.run import Run
    task_profile_file = click.format_filename(task_profile)
    cmd = Run(config_user=ctx.obj['config_user'], task_profile_file=task_profile_file, dry_run=dry_run)
    cmd.execute()


@cli.command()
@click.argument('task_id', type=int)
@click.pass_context
def show(ctx, task_id):
    from jsub.command.show import Show
    cmd = Show(config_user=ctx.obj['config_user'], task_id=task_id)
    cmd.execute()


@cli.command()
@click.argument('task_ids', type=int, nargs=-1)
@click.pass_context
def ls(ctx, task_ids):
    from jsub.command.ls import Ls
    cmd = Ls(config_user=ctx.obj['config_user'], task_ids=list(task_ids))
    cmd.execute()


@cli.command()
@click.pass_context
def package(ctx):
    from jsub.command.package import Package
    cmd = Package(config_user=ctx.obj['config_user'])
    cmd.execute()


def main():
    cli(obj={})
