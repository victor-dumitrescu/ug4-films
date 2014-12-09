import re
import json
from collections import namedtuple


Tuple = namedtuple('Tuple', 'entity, type, ss, token, type2, dependecy')


def construct_vocabulary():
    pass


def make_tuple(str):
    str = str.strip()
    m = re.search(r'(?P<entity>(e\d+|/m/\w+)):(?P<type>[tm]\.?\d+\.\d+\.\d+):(?P<ss>[\w\.]+):(?P<token>.+):(?P<type2>[map]):(?P<dependecy>\w+)', str)
    try:
        return Tuple._make(m.groups()[1:])
    except:
        print str, m.groups()
        raise


def main():

    data = {}
    path = '../../experiment/'
    with open(path + 'filtered.movies.data') as f:
        for row in f:
            m = re.search(r'(?P<id>\d+)\s+(?P<tuples>.*)\s+(?P<ents1>{.*})\s+(?P<ents2>{.*})', row)
            data[m.group('id')] = (map(make_tuple, m.group('tuples').split()),
                                   json.loads(m.group('ents1')),
                                   json.loads(m.group('ents2')))

main()
