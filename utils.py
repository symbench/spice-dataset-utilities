import subprocess
from tempfile import TemporaryDirectory
from os import path
import sys

script_dir = path.dirname(path.realpath(__file__))

def local_file(filename):
    return path.join(script_dir, filename)

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

def update_schematic(filename):
    print(f'updating {filename}', file=sys.stderr)
    cmds = ['bash', local_file('update-eeschema.sh'), filename]
    spawn(cmds)

def dialog_name(filename):
    print(f'checking {filename}', file=sys.stderr)
    dialog_name = utils.spawn(['bash', utils.local_file('print-dialog-name.sh'), filename])
    return dialog_name.strip()

