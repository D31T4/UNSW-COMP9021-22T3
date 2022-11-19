# COMP9021 22T3
# Quiz 1 *** Due Friday Week 3 @ 9.00pm
#        *** Late penalty 5% per day
#        *** Not accepted after Monday Week 4 @ 9.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION

import sys
from random import seed, randrange
from pprint import pprint

try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
mapping = {}
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 8, upper_bound)
    if r > 0:
        mapping[i] = r
print('\nThe generated mapping is:')
print('  ', mapping)
# sorted() can take as argument a list, a dictionary, a set...
keys = sorted(mapping.keys())
print('\nThe keys are, from smallest to largest: ')
print('  ', keys)

cycles = []
reversed_dict_per_length = {}

# INSERT YOUR CODE HERE
def detectCycles(graph):
    '''
    Detect cycles in a graph
    
    Arguments:
    - graph: dictionary representation of a graph

    Returns:
    - list of cycles sorted in ascending order of value of 1st pointer in each cycle
    '''
    visited_global = set()
    cycles = []

    for key in graph.keys():
        # no need to repeat if the node is visited already
        if key in visited_global:
            continue

        cycle = [key]
        visited_local = set([key])

        while True:
            pointer = graph[cycle[-1]]

            if not (pointer in graph):
                break

            if pointer in visited_local:
                break

            cycle.append(pointer)
            visited_local.add(pointer)

        # check if cycle is valid
        if cycle[0] == graph[cycle[-1]]:
            cycles.append(cycle)
            visited_global = visited_global | visited_local

    cycles.sort(key = lambda cycle: cycle[0])
    return cycles

cycles = detectCycles(mapping)

def reverseDictPerLength(graph):
    '''
    construct an inverse map of the graph

    Arguments:
    - graph: mapping function

    Returns:
    - inverse map grouped by length
    '''
    reversed_dict = {}

    # reverse dict
    for key in sorted(graph.keys()):
        value = graph[key]

        if value in reversed_dict:
            reversed_dict[value].append(key)
        else:
            reversed_dict[value] = [key]

    # group by length
    group = dict()
    for key, value in reversed_dict.items():
        length = len(value)

        if length in group:
            group[length][key] = value
        else:
            group[length] = { key: value }

    return group

reversed_dict_per_length = reverseDictPerLength(mapping)

print('\nProperly ordered, the cycles given by the mapping are: ')
print('  ', cycles)
print('\nThe (triply ordered) reversed dictionary per lengths is: ')
pprint(reversed_dict_per_length)

