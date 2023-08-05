import json
import os
import re
import subprocess
import sys

try:
    with open('personal_token.json') as f:
        data = json.load(f)
        token = data['token']
        del(data)
except FileNotFoundError:
    pass


def get_latest_versions() -> tuple[int, int, int]:
    cmd = 'git fetch --all && git show origin/developer:CHANGELOG.md'
    output = subprocess.check_output(cmd, shell=True)
    pattern = r'## (\d{1,2})\.(\d{1,2})\.(\d{1,2})'
    results = re.findall(pattern, output.decode('utf-8'))

    latest_major, latest_minor, latest_patch = [int(num) for num in results[0]]

    return latest_major, latest_minor, latest_patch


def get_new_version(args) -> str:
    latest_major, latest_minor, latest_patch = get_latest_versions()

    if len(args) == 1 or args[1] == 'patch':
        return f'{latest_major:.0f}.{latest_minor:.0f}.{latest_patch+1:.0f}'
    elif args[1] == 'major':
        return f'{latest_major+1:.0f}.0.0'
    elif args[1] == 'minor':
        return f'{latest_major:.0f}.{latest_minor+1:.0f}.0'


def get_current_branch() -> str:
    cmd = 'git rev-parse --abbrev-ref HEAD'
    output = subprocess.check_output(cmd, shell=True)
    return output.decode('utf-8').replace('\n', '')


def create_command() -> str:
    cmd = f'curl --header \"PRIVATE-TOKEN: {token}\" '
    cmd += f'--data \"version={get_new_version(sys.argv)}'
    cmd += f'&branch={get_current_branch()}\" '
    cmd += 'https://gitlab.com/api/v4/projects/31754220/repository/changelog'
    return cmd


def pre_processing():
    os.system('git fetch --all')
    os.system('git checkout origin/developer CHANGELOG.md')
    os.system('git push')


def main():
    pre_processing()
    cmd = create_command()
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    main()
