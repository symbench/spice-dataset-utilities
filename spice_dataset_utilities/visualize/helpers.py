from itertools import chain

def component_type(line):
    return line[0].upper()

def is_component_line(line):
    is_comment = line.startswith('.') or line.startswith('*')
    return not is_comment and len(line) > 0 and line[0].isalpha()

def component_lines(lines):
    return (line for line in lines[1:] if is_component_line(line))

def count_dict(items):
    counts = {}
    for item in items:
        count = counts.get(item, 0)
        counts[item] = count + 1
    return counts

def file_contents(f):
    with open(f, 'rb') as f:
        return f.read().decode('utf-8', 'ignore').split('\n')

