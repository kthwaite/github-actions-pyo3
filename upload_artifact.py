# coding: utf-8

import argparse
import glob
import json
import logging
import os
from typing import Generator

from github import Github, GithubException


log = logging.getLogger(__name__)


def find_wheels(dist_dir: os.PathLike) -> Generator[os.PathLike, None, None]:
    """Get a list of wheels in a directory.
    """
    path = os.path.join(dist_dir, "*.whl")
    for wheel in glob.glob(path):
        yield wheel


def ensure_getenv(var: str) -> str:
    """Try to fetch an environment variable, raising a RuntimeError if it does not
    exist.
    """
    try:
        return os.environ[var]
    except KeyError:
        raise RuntimeError(f'${var} is not set')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dist_dir", help="Directory to search for wheels", default="./dist"
    )
    parser.add_argument('-v', '--verbose', help='Print detailed logs')
    args = parser.parse_args()

    github_token = ensure_getenv("GITHUB_TOKEN")
    repo_name = ensure_getenv('GITHUB_REPOSITORY')
    tag_ref = ensure_getenv('GITHUB_REF')
    if not tag_ref.startswith('refs/tags'):
        raise RuntimeError(f'{tag_ref} does not look like a valid tag, aborting')
    release_tag = tag_ref.replace('refs/tags/', '')

    api = Github(github_token)
    repo = api.get_repo(repo_name)
    try:
        release = repo.get_release(release_tag)
    except GithubException as exc:
        if exc.status == 404:
            log.info('No such release exists: %s')
            log.info('Creating new release for tag: %s')
            release = repo.create_git_release(release_tag, release_tag, '')
        else:
            raise exc

    for wheel in find_wheels(args.dist_dir):
        release.upload_asset(wheel)


if __name__ == "__main__":
    main()
