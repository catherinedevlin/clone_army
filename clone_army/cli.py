# -*- coding: utf-8 -*-

import getpass
import logging

import click

from . import clone_army


@click.command(context_settings=dict(ignore_unknown_options=True, ))
@click.option(
    '-o',
    '--org',
    'type',
    flag_value='org',
    default=True,
    help='Clone GitHub account of an org')
@click.option(
    '-u',
    '--user',
    'type',
    flag_value='user',
    help='Clone GitHub account of a single user')
@click.option('-f', '--filter', help='Filter repositories (regex syntax)')
@click.option('-v', '--verbose', is_flag=True, help='See logging info')
@click.option(
    '-x',
    '--existing-only',
    is_flag=True,
    help='Only update directories already present, no new clones')
@click.option('-l', '--login', help='Username to get private repos')
@click.argument('account', default='')
@click.argument('git_options', nargs=-1, type=click.UNPROCESSED)
def main(account, type, filter, verbose, git_options, existing_only, login):
    """Console script for clone_army"""
    if account.startswith('-'):
        raise click.BadArgumentUsage("Options for Git should come at end.")
    if login:
        auth = (login, getpass.getpass())
    else:
        auth = (None, None)
    if verbose:
        logging.getLogger(__name__).setLevel(logging.INFO)
    if existing_only:
        if account or (type == 'user'):
            raise click.exceptions.BadArgumentUsage(
                'Do not specify account or type with --existing-only')
        else:
            clone_army.Repository.synch_present(filter, auth=auth)
    else:
        if not account:
            raise click.exceptions.BadArgumentUsage('Missing account name')
        clone_army.Repository.synch_all(account, type, filter, auth,
                                        *git_options)


if __name__ == "__main__":
    main()
