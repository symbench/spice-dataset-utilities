from itertools import chain
from . import helpers as h

def component_types(lines):
    return (h.component_type(l) for l in h.component_lines(lines))

def component_type_counts(*files):
    components = chain.from_iterable(( component_types(c) for c in files ))
    return h.count_dict(components)

def component_type_counts_by_netlist(*netlists):
    component_count_freqs = {}
    for netlist in netlists:
        counts = component_type_counts(netlist)
        for (component, count) in counts.items():
            count_list = component_count_freqs.get(component, [])
            count_list.append(count)
            component_count_freqs[component] = count_list

    return dict([ (comp, h.count_dict(counts)) for (comp, counts) in component_count_freqs.items() ])

if __name__ == '__main__':
    import argparse
    import sys
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument('infiles', nargs='*')
    parser.add_argument('--total', default=False, action='store_true')
    args = parser.parse_args()

    if len(args.infiles) == 0:
        files = [sys.stdin.readlines()]
    else:
        files = ( h.file_contents(f) for f in args.infiles )

    files = ( [l.strip() for l in f] for f in files )
    if args.total:
        print(json.dumps(component_type_counts(*files)))
    else:
        print(json.dumps(component_type_counts_by_netlist(*files)))
