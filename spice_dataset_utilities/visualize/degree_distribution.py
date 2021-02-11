from spice_dataset_utilities.visualize import helpers as h
from itertools import chain
from PySpice.Spice.Parser import SpiceParser

def count_node_degrees(component_set):
    node_degrees = []
    for element in component_set:
        node_degrees.append(len(element.pins))

    return node_degrees, len(component_set)

def average_degree(component_set):
    node_degrees, count = count_node_degrees(component_set)
    return sum(node_degrees) / count

def aggregate_degree_distributions(*files):
    files = ( '\n'.join(h.file_contents(f)) for f in files )
    circuits = ( parse_netlist(contents) for contents in files )
    circuits = [ circuit for circuit in circuits if circuit is not None ]

    metrics = {}
    metrics['combined'] = [ average_degree(list(chain(c.elements, c.nodes))) for c in circuits ]
    metrics['nodes'] = [ average_degree(c.nodes) for c in circuits ]
    metrics['elements'] = [ average_degree(c.elements) for c in circuits ]
    return metrics

def parse_netlist(textfile, name=None):
    try:
        parser = SpiceParser(source=textfile)
        circuit = parser.build_circuit()
        return circuit if len(circuit.elements) > 0 else None
    except:
        if name:
            print(f'invalid spice file: {name}', file=sys.stderr)
        return None

if __name__ == '__main__':
    import argparse
    import sys
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument('infiles', nargs='+')
    parser.add_argument('--total', default=False, action='store_true')
    args = parser.parse_args()

    metrics = aggregate_degree_distributions(*args.infiles)
    print(json.dumps(metrics))
