#!/usr/bin/env python

from json import loads
from subprocess import run, PIPE, DEVNULL
from sys import argv
from typing import Dict

from dictionariescomparator import DictionariesComparator


def runshell(cmd: str, verbose=False) -> None:
    """
    Returns the stdout of shell command passed in cmd argument.
    Prints stdout if verbose=True
    """
    if cmd:
        if '\n' in cmd:
            results = [
                runshell(line.strip()) 
                for line in cmd.split('\n') if line.strip()
                ]
            return results[-1]
        else:
            tokens = cmd.split(' ')
            result = run(tokens, stdout=PIPE, stderr=DEVNULL).stdout
            if verbose:
                print(result)
            return result


def get_extra_vars(job: int) -> Dict:
    """
    Returs the extra_vars of passed job as a dictionary.
    """
    extra_vars = {}
    cmd_res = runshell(f'awx-cli job get {job} -f json')
    if cmd_res:
        job_details = loads(cmd_res)['extra_vars']
        extra_vars = loads(job_details)
    return extra_vars


def compare_jobs(job_a: int, job_b: int) -> None:
    """
    Performs a comparison between the extra_vars of the jobs passed.
    """
    extra_vars_a = get_extra_vars(job_a)
    extra_vars_b = get_extra_vars(job_b)
    DictionariesComparator(extra_vars_a, extra_vars_b, job_a, job_b)


def main():
    if len(argv) == 3:
        compare_jobs(argv[1], argv[2])


if __name__ == '__main__':
    main()
