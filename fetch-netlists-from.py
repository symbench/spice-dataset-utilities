# Given a github repo, fetch/convert all the netlists from it
import shutil
import argparse
import sys
import os
from os import path
import json
import utils
import itertools

def is_schematic(filename):
    return filename.endswith('.sch')

def update_schematic(filename):
    cmds = ['bash', utils.local_file('update-eeschema.sh'), filename]
    utils.spawn(cmds)

def convert_to_netlist(filename):
    utils.spawn(['bash', utils.local_file('eeschema-to-netlist.sh'), filename])
    netlist = filename.replace('.sch', '.cir')
    if path.exists(netlist):
        return (filename, netlist)
    else:
        return (filename, None)

def list_schematics(dirname):
    paths_to_search = ( path.join(dirname, name) for name in os.listdir(dirname) )
    schematics = []
    for name in paths_to_search:
        if path.isdir(name):
            schematics.extend(list_schematics(name))
        elif is_schematic(name):
            schematics.append(name)

    return schematics

def move_file(src_path, target_dir):
    basename = path.basename(src_path)
    filename = basename
    existing_files = os.listdir(target_dir)
    index = 2
    while filename in existing_files:
        filename = basename + str(index)
        index += 1

    dst_path = path.join(target_dir, filename)
    shutil.move(src_path, dst_path)
    return filename

def convert_schematics(save_dir, schematics):
    for schematic in schematics:
        update_schematic(schematic)

    netlists = (convert_to_netlist(schematic) for schematic in schematics)
    return netlists

def log_results(url, save_dir, netlists, record_file, error_file):
    for (filename, netlist) in netlists:
        success = netlist is not None
        rel_filename = filename.replace(work_dir, '')
        if success:
            print(f'CONVERTED {rel_filename}', file=sys.stderr)
            relative_src = netlist.replace(work_dir, '')
            dst_file = move_file(netlist, save_dir)
            record_file.write(json.dumps({
                'type': 'KiCad',
                'schematic': rel_filename,
                'netlist_src': relative_src,
                'netlist': dst_file,
                'repo_url': url,
            }) + '\n')
        else:
            dialog_name = utils.dialog_name(filename)
            print(f'FAILED to convert {rel_filename}: {dialog_name}', file=sys.stderr)
            error_file.write(json.dumps({
                'type': 'KiCad',
                'schematic': rel_filename,
                'repo_url': url,
                'dialog_name': dialog_name,
            }) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', help='Repository URLs to search for schematics', nargs='*')
    parser.add_argument('--out', default='.')
    parser.add_argument('--error_file', default='errors.jsonl')
    parser.add_argument('--json', default=False, action='store_true')
    args = parser.parse_args()
    inputs = sys.stdin if len(args.urls) == 0 else args.urls

    records = open(path.join(args.out, 'records.jsonl'), 'a')
    errors = open(path.join(args.out, args.error_file), 'a')

    if args.json:
        infos = ( json.loads(line) for line in inputs )
        for (repo, infos) in itertools.groupby(infos, lambda info: info['repo_url']):
            with utils.fetch_repo(repo) as work_dir:
                schematics = [ work_dir + info['schematic'] for info in infos ]
                netlists = convert_schematics(args.out, schematics)
                log_results(repo, args.out, netlists, records, errors)

    else:
        for url in inputs:
            with utils.fetch_repo(url) as work_dir:
                schematics = list_schematics(work_dir)
                netlists = convert_schematics(args.out, schematics)
                log_results(repo, args.out, netlists, records, errors)

    records.close()
    errors.close()
