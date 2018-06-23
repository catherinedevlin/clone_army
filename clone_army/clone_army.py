# -*- coding: utf-8 -*-

import itertools
import logging
import os.path
import re
import subprocess

import click
import requests

_REPO_LIST_URL = 'https://api.github.com/{type}s/{account}/repos?page={page_no}'


def repositories(account, type='org', filter=None, auth=(None, None)):
    for page_no in itertools.count(1):
        click.echo('Page {page_no}'.format(page_no=page_no))
        url = _REPO_LIST_URL.format(
            type=type, account=account, page_no=page_no, filter=filter)
        logging.info('Getting repo list from {}'.format(url))
        resp = requests.get(url, auth=auth)
        resp.raise_for_status()
        if not resp.json():
            raise StopIteration
        for repo in resp.json():
            if auth or not repo['private']:
                if (not filter) or re.search(filter, repo['name']):
                    yield repo


class Repository(object):
    def __init__(self, data):
        self.__dict__.update(data)

    def authorized_clone_url(self, auth):
        """Generates a version of clone url with embedded auth

        Warning: exposes password visibly
        """

        (protocol, sep, path) = self.clone_url.partition('://')
        return f'{protocol}{sep}{auth[0]}:{auth[1]}@{path}'

    @classmethod
    def synch_all(cls, account, type, filter=None, auth=(None, None), *args):
        """
        Clones or updates repositories belonging to `account`.
        """
        for repo_data in repositories(account, type, filter, auth=auth):
            repo = cls(repo_data)
            repo.synch(auth, *args)

    @classmethod
    def synch_present(cls, filter=None, auth=(None, None), *args):
        """
        Updates repositories already present in child directories.
        """
        for dir in os.listdir():
            if os.path.isdir(dir):
                if filter and not re.search(filter, dir):
                    logging.info(f'{dir} ignored; filtered by `{filter}`')
                else:
                    logging.info(f'{dir} exists; pulling changes')
                    subprocess.run(['git', 'pull'], cwd=dir)

    def synch(self, auth=(None, None), *args):
        if os.path.exists(self.name):
            logging.info(f'{self.name} exists; pulling changes')
            subprocess.run(['git', 'pull'], cwd=self.name)
        else:
            logging.info(f'Cloning {self.name}')
            subprocess.run(
                ['git', 'clone', *args,
                 self.authorized_clone_url(auth)])
