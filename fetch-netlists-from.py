# Given a github repo, fetch/convert all the netlists from it
from tempfile import TemporaryDirectory
import subprocess
import shutil
import argparse
import sys
import os
from os import path
script_dir = path.dirname(path.realpath(__file__))

def local_file(filename):
    return path.join(script_dir, filename)

def is_schematic(filename):
    return filename.endswith('.sch')

def spawn(cmds):
    print('--> about to run', ' '.join(cmds))
    try:
        subprocess.run(cmds, stdout=subprocess.PIPE, timeout=5)
    except:
        print('Timeout exceeded')

def update_schematic(filename):
    cmds = ['bash', local_file('update-eeschema.sh'), filename]
    spawn(cmds)

def convert_to_netlist(filename):
    spawn(['bash', local_file('eeschema-to-netlist.sh'), filename])
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

def fetch_repo(url, save_dir):
    print('about to fetch', url)
    with TemporaryDirectory() as work_dir:
        print('work_dir', work_dir)
        spawn(['git', 'clone', '--recurse-submodules', url, work_dir])
        print('cloned results to', work_dir)
        schematics = list_schematics(work_dir)
        for schematic in schematics:
            update_schematic(schematic)

        netlists = (convert_to_netlist(schematic) for schematic in schematics)
        records = open(path.join(save_dir, 'records.txt'), 'w+')
        error_file = open(path.join(save_dir, 'errors.txt'), 'w+')
        for (filename, netlist) in netlists:
            success = netlist is not None
            if success:
                relative_src = netlist.replace(work_dir, '')
                dst_file = move_file(netlist, save_dir)
                records.write(f'{dst_file}\t{relative_src}\t{url}\n')
            else:
                error_file.write(f'{filename}\t{url}\n')
        records.close()
        error_file.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', help='Repository URLs to search for schematics', nargs='+')
    parser.add_argument('--out', default='.')
    args = parser.parse_args()

    for url in args.urls:
        print('-- FETCHING', url)
        fetch_repo(url, args.out)
