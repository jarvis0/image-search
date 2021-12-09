# -*- coding: utf-8 -*-

import sys
from configparser import ConfigParser
from subprocess import call
from typing import List


def read_current_version(setup_file) -> List[int]:
    version = setup_file.get('project', 'version')
    return [int(n) for n in version.split('.')]


def increment_version(current_version_as_list: List[int], increment: str) -> str:
    new_version = None
    major, minor, patch = current_version_as_list
    if increment == 'patch':
        new_version = [major, minor, patch + 1]
    if increment == 'minor':
        new_version = [major, minor + 1, 0]
    if increment == 'major':
        new_version = [major + 1, 0, 0]

    return '.'.join([str(n) for n in new_version])


def confirm_version(new_version):
    confirm = input(f'Publishing version {new_version}. Confirm [y/N]: ')
    if confirm not in {'y', 'Y', 'yes', 'YES'}:
        print('\nExited by user.\n')
        sys.exit(0)


def validate_increment(increment: str) -> None:
    if increment in {'patch', 'minor', 'major'}:
        return
    print('Usage: python -m scripts.version [major|minor|patch]')
    sys.exit(1)


def write_version(setup_file, new_version):
    setup_file.set('project', 'version', new_version)
    with open('setup.cfg', 'w') as f:
        setup_file.write(f)


def write_changelog(setup_file, old_version):
    with open('CHANGELOG.md', 'r') as f:
        changelog = f.readlines()

    with open('CHANGELOG.md', 'w') as f:
        repo = setup_file.get('gitlab', 'repository_url')
        version = setup_file.get('project', 'version')
        for line in changelog:
            if line.startswith('## [Unreleased]'):
                f.write(f'## [Unreleased]\n')
                f.write('\n')
                f.write(f'## [{version}]({repo}/compare/v{old_version}...v{version})\n')
            else:
                f.write(line)


def main():
    try:
        increment = sys.argv[1]
    except IndexError:
        increment = 'invalid'

    validate_increment(increment)

    setup_file = ConfigParser()
    setup_file.read('setup.cfg')
    project_name = setup_file.get('project', 'name')

    current_version_as_list = read_current_version(setup_file)
    current_version = '.'.join([str(num) for num in current_version_as_list])
    new_version = increment_version(current_version_as_list, increment)
    confirm_version(new_version)
    write_version(setup_file, new_version)
    write_changelog(setup_file, current_version)

    # Commit.
    call(['git', 'add', 'CHANGELOG.md', 'setup.cfg'])
    call(['git', 'commit', '-m', f'{project_name} v{new_version}'])
    call(['git', 'push'])

    # Release tag.
    call(['git', 'tag', '-a', f'v{new_version}', '-m', f'{project_name} v{new_version}'])
    call(['git', 'push', '--follow-tags'])


if __name__ == '__main__':
    main()
