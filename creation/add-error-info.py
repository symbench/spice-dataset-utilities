import argparse
import json
import sys
from os import path
import itertools
import utils

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('errorfile', help='Error file generated from fetch-netlists-from', type=argparse.FileType('r'), nargs='?')
    args = parser.parse_args()

    inputs = args.errorfile if args.errorfile is not None else sys.stdin
    infos = ( json.loads(line) for line in inputs )
    for (repo, infos) in itertools.groupby(infos, lambda info: info['repo_url']):
        infos = list(infos)
        with utils.fetch_repo(repo) as work_dir:
            for info in infos:
                filename = work_dir + info['schematic']
                utils.update_schematic(filename)

            for info in infos:
                filename = work_dir + info['schematic']
                info['dialog_name'] = utils.dialog_name(filename)
                print(json.dumps(info))
