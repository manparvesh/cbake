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


def green_output(s):
    click.echo(CBAKE_PREFIX + chalk.green(s))


def red_output(s):
    click.echo(CBAKE_PREFIX + chalk.red(s))


def print_empty_line():
    click.echo(CBAKE_PREFIX)


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
        green_output('Building project...')
        print_empty_line()
        config_content = yaml.load(open(bake_file_path))
        executables = config_content.get('executables')
        directory_with_space = " " + directory
        build_successful = True
        for executable in executables:
            command_string = "gcc " + (directory if len(executables) is not 0 else "") + directory_with_space.join(
                executables[executable]) + " -o " + ouput_directory + executable
            green_output("Building executable: " + executable)
            query_result = os.system(command_string)
            if query_result == 0:
                green_output("Successfully built executable: " + executable)
            else:
                red_output("Compilation failed")
                build_successful = False
            print_empty_line()
        if build_successful:
            green_output("Successfully built project: " + config_content.get('project'))
        else:
            red_output("There were build errors")
    else:
        red_output('No .bake.yml file in specified directory')
