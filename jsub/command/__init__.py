import click

@click.group()
@click.option('--jsubrc', default='~/.jsubrc', help='Configuration file to run JSUB with.')
@click.pass_context
def cli(ctx, jsubrc):
	ctx.obj['jsubrc'] = jsubrc

@cli.command()
def version():
	"""Show the version of the software."""
	from jsub import version as jsub_version
	click.echo('JSUB version: %s' % jsub_version())


@cli.command()
@click.argument('task_id', type=int)
@click.argument('new_name', type=str)
@click.pass_context
def rename(ctx, task_id, new_name):
	"""Rename a task."""
	from jsub.command.rename import Rename
	cmd = Rename(jsubrc=ctx.obj['jsubrc'], task_id=task_id, new_name=new_name)
	cmd.execute()


@cli.command()
@click.argument('task_profile', type=click.Path(exists=True))
@click.pass_context
def create(ctx, task_profile):
	"""Create a task from a task description file."""
	from jsub.command.create import Create
	task_profile_file = click.format_filename(task_profile)
	cmd = Create(jsubrc=ctx.obj['jsubrc'], task_profile_file=task_profile_file)
	cmd.execute()


@cli.command()
@click.option('--dry-run', is_flag=True, help='Create necessary files without final submission.')
@click.option('--resubmit','-r' , is_flag=True, help='Enforce resubmission if the task has already been submitted, deleting orginal jobs.')
@click.argument('task_id', type=int)
@click.pass_context
def submit(ctx, dry_run, task_id, resubmit):
	"""Submit a task to backend."""
	from jsub.command.submit import Submit
	cmd = Submit(jsubrc=ctx.obj['jsubrc'], task_id=task_id, dry_run=dry_run, resubmit=resubmit)
	cmd.execute()

@cli.command()
@click.option('--dry-run', is_flag=True, help='Create necessary files without final submission.')
@click.argument('task_id', type=int)
@click.pass_context
def resubmit(ctx, dry_run, task_id):
	"""Equivalent to 'jsub submit -r' command"""
	from jsub.command.submit import Submit
	cmd = Submit(jsubrc=ctx.obj['jsubrc'], task_id=task_id, dry_run=dry_run, resubmit=True)
	cmd.execute()

@cli.command()
@click.option('--force','-f' , is_flag=True, help='Force deleting a submitted task.')
@click.argument('task_id', type=int)
@click.pass_context
def remove(ctx, force, task_id):
	"""Delete a task."""
	from jsub.command.remove import Remove
	cmd = Remove(jsubrc=ctx.obj['jsubrc'], task_id=task_id, force=force)
	cmd.execute()

@cli.command()
@click.argument('task_id', type=int)
@click.option('--sub_id','-i', type=int, default=None, help='Specifying a subjob id to inspect.')
@click.option('--jobvar','-j' , type=str, default=None, help='Specifying a jobvar list to look at.')
@click.option('--max_cycle','-n' , type=int, default=20, help='Maximum length of jobvar list to display')
@click.pass_context
def jobvar(ctx, task_id,sub_id=None,jobvar=None, max_cycle=20):
	"""View the values of jobvar lists"""
	from jsub.command.jobvar import Jobvar
	cmd = Jobvar(jsubrc=ctx.obj['jsubrc'], task_id=task_id, sub_id=sub_id, jobvar=jobvar, max_cycle=max_cycle)
	cmd.execute()




@cli.command()
@click.argument('task_id', type=int)
@click.option('--status', '-s', type=str, default=None, help ='List the subjobs with matched running state.')
@click.option('--silent', is_flag=True, help='Update task status info without printing message.')
@click.pass_context
def status(ctx, task_id, status=None, silent=False):
	"""Show the backend status of a task."""
	from jsub.command.status import Status
	cmd = Status(jsubrc=ctx.obj['jsubrc'], task_id=task_id, states=status, silent=silent)
	cmd.execute()


@cli.command()
@click.option('--dry-run', is_flag=True, help='Create necessary files without final submission')
@click.argument('task_profile', type=click.Path(exists=True))
@click.pass_context
def run(ctx, dry_run, task_profile):
	"""Create from a task profile, and submit."""
	from jsub.command.run import Run
	task_profile_file = click.format_filename(task_profile)
	cmd = Run(jsubrc=ctx.obj['jsubrc'], task_profile_file=task_profile_file, dry_run=dry_run)
	cmd.execute()


@cli.command()
@click.argument('task_id', type=int)
@click.option('--dump', '-d', type=str, default='', help ='Dump task file to given path')
@click.pass_context
def show(ctx, task_id, dump):
	"""Show detailed description of a task."""
	from jsub.command.show import Show
	cmd = Show(jsubrc=ctx.obj['jsubrc'], task_id=task_id, dump = dump)
	cmd.execute()


@cli.command()
@click.argument('task_ids', type=int, nargs=-1)
@click.option('--update/--no-update','-u/-n' , is_flag=True, default = True, help='Whether to update info in task_repo.')
@click.pass_context
def ls(ctx, task_ids, update):
	"""List all tasks."""
	from jsub.command.ls import Ls
	cmd = Ls(jsubrc=ctx.obj['jsubrc'], task_ids=list(task_ids), update = update)
	cmd.execute()


@cli.command()
@click.pass_context
def package(ctx):
	"""Show active packages."""
	from jsub.command.package import Package
	cmd = Package(jsubrc=ctx.obj['jsubrc'])
	cmd.execute()

@cli.command()
@click.pass_context
@click.argument('task_id', type=int)
@click.option('--sub_id', '-i', type=str, default='', help ='Filter the sub_ids of the jobs that you want to fetch log files, separate numbers with comma.')
@click.option('--status', '-s', type=str, default='', help ='Filter the status of the jobs that you want to fetch log files (DFWRO)')
@click.option('--njobs', '-n', type=str, help ='The maximum number of jobs for log retrieval. (10 by default)')
@click.option('--path', '-p', type=str, default='', help ='The path to which to dump log files, jsub task dir by default.')
def getlog(ctx, task_id,  sub_id ,path, status, njobs):
	"""Retrieve log files of selected subjobs."""
	from jsub.command.getlog import Getlog
	cmd = Getlog(jsubrc=ctx.obj['jsubrc'], task_id = task_id, sub_id = sub_id, path = path, status = status, njobs = njobs)
	cmd.execute()

@cli.command()
@click.argument('task_id', type=int)
@click.option('--done' ,'-d' , is_flag=True, default = False, help='reschedule jobs with Done status')
@click.option('--failed' ,'-f' , is_flag=True, default = False, help='reschedule jobs with Failed status')
@click.option('--running' ,'-r' , is_flag=True, default = False, help='reschedule jobs with Running status')
@click.option('--waiting' ,'-w' , is_flag=True, default = False, help='reschedule jobs with Waiting status')
@click.option('--status' ,'-s' , type=str, default = '', help='reschedule jobs with given status (Done/Failed/Running/Waiting)')
@click.option('--sub_id', '-i', type=str, default='', help ='List the subjobs with matched sub IDs, separate numbers with comma.')
@click.option('--backend_id', '-b', type=str, default='', help ='List the subjobs with matched backend job IDs, separate numbers with comma.')
@click.pass_context

def reschedule(ctx, task_id, done, failed, running, waiting, sub_id, backend_id,status):
	"""Reschedule selected subjobs."""
	from jsub.command.reschedule import Reschedule
	status_out=''
	for x in ['done','waiting','running','failed']:
		if x in status:
			status_out+=x[0].upper()
	if failed:
		status_out+='F'
	if running:
		status_out+='R'
	if waiting:
		status_out+='W'
	if done:
		status_out+='D'
	
	cmd = Reschedule(jsubrc=ctx.obj['jsubrc'], task_id=task_id, status=status_out, sub_id=sub_id, backend_id=backend_id)
	cmd.execute()

@cli.command()
@click.argument('input_list', type=click.Path(exists=True))
@click.pass_context
def register(ctx, input_list):
	"""Upload files to SE and register them to DFC. INPUT_LIST should be a text file that contains the names of relevant files."""
	from jsub.command.register_to_dfc import RegisterToDFC
	input_list = click.format_filename(input_list)
	cmd = RegisterToDFC(jsubrc=ctx.obj['jsubrc'], input_list=input_list)
	cmd.execute()





def main():
	cli(obj={})
