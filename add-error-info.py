from tempfile import TemporaryDirectory
import argparse
import json
import subprocess
import sys
from os import path
import itertools
script_dir = path.dirname(path.realpath(__file__))

def spawn(cmds):
    try:
        result = subprocess.run(cmds, timeout=5, capture_output=True)
        return result.stdout.decode()
    except Exception as e:
        return 'Timeout exceeded'

def fetch_repo(url):
    print(f'fetching {url}', file=sys.stderr)
    work_dir = TemporaryDirectory()
    spawn(['git', 'clone', '--recurse-submodules', url, work_dir.name])
    return work_dir

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('errorfile', help='Error file generated from fetch-netlists-from', type=argparse.FileType('r'), nargs='?')
    args = parser.parse_args()

    inputs = args.errorfile if args.errorfile is not None else sys.stdin
    infos = ( json.loads(line) for line in inputs )
    for (repo, infos) in itertools.groupby(infos, lambda info: info['repo_url']):
        with fetch_repo(repo) as work_dir:
            for info in infos:
                filename = work_dir + info['schematic']
                print(f'checking {filename}', file=sys.stderr)
                dialog_name = spawn(['bash', path.join(script_dir, 'print-dialog-name.sh'), filename])
                info['dialog_name'] = dialog_name.strip()
                print(json.dumps(info))
