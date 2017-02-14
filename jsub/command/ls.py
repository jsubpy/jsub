import datetime

import click

from jsub import Jsub


COLUMN_TITLE = {
    'task_id':    'Task ID',
    'name':       'Name',
    'app':        'Application',
    'backend':    'Backend',
    'status':     'Status',
    'created_at': 'Creation Time (UTC)',
}


def _convert_table_data(tasks_data, columns):
    table_data = []
    for task_data in tasks_data:
        line_data = []
        for col in columns:
            if col not in task_data:
                line_data.append('N/A')
                continue

            if col in ['app', 'backend']:
                if 'type' in task_data[col]:
                    line_data.append(task_data[col]['type'])
                else:
                    line_data.append(str(task_data[col]))
            elif col in ['created_at']:
                created_time = datetime.datetime.strptime(task_data[col], '%Y-%m-%dT%H:%M:%S.%f')
                time_str = datetime.datetime.strftime(created_time, '%Y-%m-%d %H:%M:%S')
                line_data.append(time_str)
            else:
                line_data.append(str(task_data[col]))
        table_data.append(line_data)
    return table_data

def _print_header(columns, widths):
    for col, w in zip(columns, widths):
        fmt = '%%-%ds' % w
        click.echo(fmt % COLUMN_TITLE[col], nl=False)
        click.echo(' ', nl=False)
    click.echo('')

def _print_hr(widths):
    for w in widths:
        click.echo('-'*w, nl=False)
        click.echo(' ', nl=False)
    click.echo('')

def _print_data(table_data, widths):
    for line_data in table_data:
        for data, w in zip(line_data, widths):
            fmt = '%%-%ds' % w
            click.echo(fmt % data, nl=False)
            click.echo(' ', nl=False)
        click.echo('')

def _print_table(table_data, columns):
    widths = []
    index = 0
    for col in columns:
        width = len(COLUMN_TITLE[col])
        for data in table_data:
            width = max(width, len(data[index]))
        widths.append(width+1)
        index += 1

    _print_header(columns, widths)
    _print_hr(widths)
    _print_data(table_data, widths)


class Ls(object):
    def __init__(self, jsubrc, task_ids):
        self.__jsubrc   = jsubrc
        self.__task_ids = task_ids if len(task_ids) else None

    def execute(self):
        j = Jsub(self.__jsubrc)
        tasks_data = j.ls(self.__task_ids)

        columns = ['task_id', 'name', 'app', 'backend', 'status', 'created_at']

        table_data = _convert_table_data(tasks_data, columns)
        _print_table(table_data, columns)
