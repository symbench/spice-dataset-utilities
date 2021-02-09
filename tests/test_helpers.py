from spice_dataset_utilities.visualize import helpers as h

def test_sort_dict():
    unsorted = {2: 'a', 3: 'b', 1: 'c'}
    sorted_d = h.sort_dict(unsorted)
    for (actual, expected) in zip(sorted_d.keys(), sorted(unsorted.keys())):
        assert actual == expected

def test_count_dict():
    unsorted = [ 2, 2, 1, 1, 3, 3]
    sorted_d = h.count_dict(unsorted)
    for (actual, expected) in zip(sorted_d.keys(), [1,2,3]):
        assert actual == expected
