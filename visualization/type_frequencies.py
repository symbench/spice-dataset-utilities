from itertools import chain
# TODO: implement function getting the type frequencies

def component_type(line):
    return line[0].upper()

def is_component_line(line):
    is_comment = line.startswith('.') or line.startswith('*')
    return not is_comment and len(line) > 0 and line[0].isalpha()

def component_lines(lines):
    return (line for line in lines[1:] if is_component_line(line))

def component_types(lines):
    return (component_type(l) for l in component_lines(lines))

def component_type_counts(*files):
    components = chain.from_iterable(( component_types(c) for c in files ))
    return count_dict(components)

def count_dict(items):
    counts = {}
    for item in items:
        count = counts.get(item, 0)
        counts[item] = count + 1
    return counts

def component_type_counts_by_netlist(*netlists):
    component_count_freqs = {}
    for netlist in netlists:
        counts = component_type_counts(netlist)
        for (component, count) in counts.items():
            count_list = component_count_freqs.get(component, [])
            count_list.append(count)
            component_count_freqs[component] = count_list

    return dict([ (comp, count_dict(counts)) for (comp, counts) in component_count_freqs.items() ])

def file_contents(f):
    with open(f, 'r') as f:
        return f.readlines()

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
        files = ( file_contents(f) for f in args.infiles )

    files = ( [l.strip() for l in f] for f in files )
    if args.total:
        print(json.dumps(component_type_counts(*files)))
    else:
        print(json.dumps(component_type_counts_by_netlist(*files)))
