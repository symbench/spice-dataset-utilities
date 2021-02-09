#! /usr/bin/env python3
# TODO: get various metrics and generate a summary HTML
import argparse
import sys
import json

parser = argparse.ArgumentParser()
parser.add_argument('infile', nargs='?')
parser.add_argument('--labels-first', default=False, action='store_true')
args = parser.parse_args()

input = sys.stdin if args.infile is None else args.infile
data = [ line.strip().split(' ') for line in input ]
if args.labels_first:
    values = [ float(pt.pop(-1)) for pt in data ]
else:
    values = [ float(pt.pop(0)) for pt in data ]
labels = [ ' '.join(pt) for pt in data ]
bar_data = {}
bar_data['x'] = labels
bar_data['y'] = values
bar_data['type'] = 'bar'
print(json.dumps(bar_data))
