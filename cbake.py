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
VERBOSE_PREFIX = CBAKE_PREFIX + "[v] "


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


def print_empty_line_verbose(verbose):
    """
    Prints an empty line with the prefix [cbake] only when verbose mode is on
    """
    if verbose:
        click.echo(VERBOSE_PREFIX)


def verbose_print(verbose, s):
    """
    Prints output with [cbake] [v] (denoting verbose mode) as prefix and in color green
    :param s: input string
    :param verbose: boolean that is set to true if verbose mode is on
    """
    if verbose:
        click.echo(VERBOSE_PREFIX + s)


obj = {}


@click.group(invoke_without_command=True)
@click.pass_context
@click.argument('directory', nargs=1, required=False)
@click.option('-o', '--output-directory', default='./')
@click.option('-v', '--verbose', is_flag=True)
def main(ctx, directory, output_directory, verbose):
    """
    Simple build tool for the C language

    More information at https://github.com/manparvesh/cbake
    """
    input_directory = directory if directory is not None else '.'
    input_directory = input_directory + '/' if not input_directory.endswith('/') else input_directory
    bake_file_path = input_directory + BAKE_FILE

    output_directory = output_directory if output_directory is not None else '.'
    output_directory = output_directory + '/' if not output_directory.endswith('/') else output_directory

    verbose_print(verbose, 'Invoked without subcommand')
    verbose_print(verbose, "Verbose: On")
    verbose_print(verbose, "Input directory: " + input_directory)
    verbose_print(verbose, "Output directory: " + output_directory)
    print_empty_line_verbose(verbose)

    if ctx.invoked_subcommand is None:
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

                command_string = config_content.get('compile') + " " + source_code_files + " -o " + output_directory \
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
    else:
        verbose_print(verbose, 'Invoked subcommand: %s' % ctx.invoked_subcommand)

        # save values to obj
        global obj
        obj['verbose'] = verbose
        obj['input_directory'] = input_directory
        obj['output_directory'] = output_directory


@main.command()
@click.pass_context
def test(ctx):
    """
    Testing command for cbake
    """
    verbose = obj['verbose']
    input_directory = obj['input_directory']
    output_directory = obj['output_directory']

    bake_file_path = input_directory + BAKE_FILE
    config_content = yaml.load(open(bake_file_path))
    executables = config_content.get('executables')

    if config_content.get('testing'):
        green_output("Testing project: " + config_content.get('project'))

        all_executables_defined = True

        for test_name in config_content.get('tests'):
            if test_name not in executables:
                red_output("Executable not defined" + test_name)
                all_executables_defined = False
            else:
                if not isfile(output_directory + test_name + ".o"):
                    red_output(test_name + " is not compiled. Compiling now")

                    executable_name = test_name + ".o"
                    source_code_files = " ".join(input_directory + x for x in executables[test_name])
                    flags = " ".join("-" + x for x in config_content.get('flags'))

                    command_string = config_content.get('compile') + " " + source_code_files + " -o " + \
                                     output_directory + executable_name + " " + flags
                    query_result = os.system(command_string)
                    if query_result == 0:
                        green_output("Successfully built executable: " + executable_name)
                    else:
                        red_output("Compilation failed")

        number_of_tests = len(config_content.get('tests'))
        str_number_of_tests = str(number_of_tests)
        failed_tests = 0

        if all_executables_defined:
            for test_name in config_content.get('tests'):
                green_output("Running: " + test_name)
                test_run_result = os.system(output_directory + test_name + ".o")
                if test_run_result == 0:
                    green_output("Test successfull: " + test_name)
                else:
                    red_output("Test failed: " + test_name)
                    failed_tests += 1

            # print result
            if failed_tests == 0:
                green_output(str_number_of_tests + " of " + str_number_of_tests + " tests ran successfully!")
            else:
                green_output(
                    str(number_of_tests - failed_tests) + " of " + str_number_of_tests + " tests ran successfully")
                red_output(str(failed_tests) + " of " + str_number_of_tests + " tests ran successfully!")
        else:
            red_output("Some executables were not defined in the config")
    else:
        red_output("Testing not enabled in config")
