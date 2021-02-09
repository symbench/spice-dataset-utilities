from spice_dataset_utilities.visualize.component_counts import component_counts_by_netlist
from spice_dataset_utilities.visualize import helpers as h
from spice_dataset_utilities.visualize.type_frequencies import component_type_counts, component_type_counts_by_netlist
import os
from os import path
import json

scriptdir = path.dirname(path.realpath(__file__))

with open(path.join(scriptdir, 'templates', 'dataset_metrics.html'), 'r') as f:
    html_template = f.read()

def find_netlists(rootdir):
    netlist_paths = []
    for file_or_dir in (path.join(rootdir, c) for c in os.listdir(rootdir)):
        if path.isdir(file_or_dir):
            contained_paths = find_netlists(file_or_dir)
            netlist_paths.extend(contained_paths)
        elif file_or_dir.endswith('.cir') or file_or_dir.endswith('.net'):
            netlist_paths.append(file_or_dir)

    return netlist_paths


def create_html(name, dataset_metrics):
    args = {'name': name, 'metrics': json.dumps(dataset_metrics)}
    return html_template.replace('$name', name).replace(
        '$metrics',
        json.dumps(dataset_metrics)
    )

def prep(files):
    files = ( h.file_contents(f) for f in files )
    return ( [l.strip() for l in f] for f in files )

if __name__ == '__main__':
    import argparse
    import sys
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_dir')
    parser.add_argument('--name')
    args = parser.parse_args()

    name = args.name if args.name != None else path.basename(args.dataset_dir)
    files = find_netlists(args.dataset_dir)

    metrics = {}
    metrics['componentCounts'] = component_counts_by_netlist(*prep(files))
    metrics['componentTypeCounts'] = component_type_counts(*prep(files))
    metrics['componentTypeCountsByNetlist'] = component_type_counts_by_netlist(*prep(files))

    print(create_html(name, metrics))
