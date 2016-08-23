#!/usr/bin/env python

import click

@click.group()
def cli():
    pass

@cli.command()
def create():
    click.echo('Creating')

@cli.command()
def submit():
    click.echo('Creating')

def main():
    cli()

if __name__ == '__main__':
    main()
