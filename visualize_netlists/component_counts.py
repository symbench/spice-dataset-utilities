from itertools import chain
from . import helpers as h

def component_counts_by_netlist(*files):
    component_counts = ( len(h.component_lines(c)) for c in files )
    return count_dict(component_counts)

if __name__ == '__main__':
    import argparse
    import sys
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument('infiles', nargs='*')
    args = parser.parse_args()

    if len(args.infiles) == 0:
        files = [sys.stdin.readlines()]
    else:
        files = ( h.file_contents(f) for f in args.infiles )

    files = ( [l.strip() for l in f] for f in files )
    print(json.dumps(component_counts_by_netlist(*files)))
