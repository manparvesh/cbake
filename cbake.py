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
CBAKE_PREFIX = '[cbake] '


@click.command()
@click.argument('directory', nargs=1, required=False)
@click.option('-o', '--ouput-directory', default='./')
def main(directory, ouput_directory):
    """
    Simple build tool for the C language

    More information at https://github.com/manparvesh/cbake
    """
    input_directory = directory if directory is not None else '.'
    input_directory = input_directory + '/' if not input_directory.endswith('/') else input_directory
    bake_file_path = input_directory + BAKE_FILE

    ouput_directory = ouput_directory if ouput_directory is not None else '.'
    ouput_directory = ouput_directory + '/' if not ouput_directory.endswith('/') else ouput_directory

    if isfile(bake_file_path):
        click.echo(chalk.green(CBAKE_PREFIX + 'Building project...'))
        config_content = yaml.load(open(bake_file_path))
        executables = config_content.get('executables')
        directory_with_space = " " + directory
        for executable in executables:
            command_string = "gcc " + (directory if len(executables) is not 0 else "") + directory_with_space.join(
                executables[executable]) + " -o " + ouput_directory + executable
            print(command_string)
            os.system(command_string)
    else:
        click.echo(chalk.red(CBAKE_PREFIX + 'No .bake.yml file in specified directory'))
