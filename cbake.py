# coding=utf-8
import os

import chalk
import yaml

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from os.path import isfile

import click


BAKE_FILE = '.bake.yml'


@click.command()
@click.argument('directory', nargs=1, required=False)
def main(directory):
    """
    Simple build tool for the C language

    More information at https://github.com/manparvesh/cbake
    """
    directory = directory if directory is not None else '.'
    directory = directory + '/' if not directory.endswith('/') else directory
    bake_file_path = directory + BAKE_FILE

    if isfile(bake_file_path):
        click.echo(chalk.green('Building project...'))
        # TODO read config file, build, etc
        config_content = yaml.load(open(bake_file_path))
        executables = config_content.get('executables')
        for executable in executables:
            os.system("gcc " + " ".join(executables[executable]) + " -o " + executable)
    else:
        click.echo(chalk.red('No .bake.yml file found in this directory'))
