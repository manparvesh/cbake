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
    """
    Prints output with [cbake] as prefix and in color green
    :param s: input string
    """
    click.echo(CBAKE_PREFIX + chalk.green(s))


def red_output(s):
    """
    Prints output with [cbake] as prefix and in color red
    :param s: input string
    """
    click.echo(CBAKE_PREFIX + chalk.red(s))


def print_empty_line():
    """
    Prints an empty line with the prefix [cbake]
    """
    click.echo(CBAKE_PREFIX)


def verbose_print(verbose, s):
    """
    Prints output with [cbake] [v] (denoting verbose mode) as prefix and in color green
    :param s: input string
    :param verbose: boolean that is set to true if verbose mode is on
    """
    if verbose:
        click.echo(CBAKE_PREFIX + "[v] " + s)


@click.command()
@click.argument('directory', nargs=1, required=False)
@click.option('-o', '--ouput-directory', default='./')
@click.option('-v', '--verbose', is_flag=True)
def main(directory, ouput_directory, verbose):
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
        flags = " ".join("-" + x for x in config_content.get('flags'))
        build_successful = True
        for executable in executables:
            executable_name = executable + ".o"
            source_code_files = " ".join(directory + x for x in executables[executable])

            command_string = config_content.get('compile') + " " + source_code_files + " -o " + ouput_directory \
                             + executable_name + " " + flags

            verbose_print(verbose, "Executing command:")
            verbose_print(verbose, command_string)
            green_output("Building executable: " + executable_name)

            query_result = os.system(command_string)
            if query_result == 0:
                green_output("Successfully built executable: " + executable_name)
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
