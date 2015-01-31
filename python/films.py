import re
import glob
import numpy as np
import cPickle as pickle
import xml.etree.ElementTree as ET
from personas import Persona
from collections import defaultdict


class Film:

    def __init__(self, id, title, fb, personas, chars):
        self.title = title
        self.id = id
        self.fb = fb
        self.personas = personas
        self.chars = chars
        self.gexf = None
        self.script_chars = None

    @property
    def gexf(self):
        return self.gexf

    @gexf.setter
    def gexf(self, value):
        self.gexf = value

    @property
    def script_chars(self):
        return self.script_chars

    @script_chars.setter
    def script_chars(self, value):
        self.script_chars = value


def match_char_names(films):

    path = '../output/'
    for id in films:

        #get character names in the script file
        script_chars = []
        with open(path + films[id].gexf) as g:
            root = ET.parse(g).getroot()
            nodes = root[1][0]
            for node in nodes:
                script_chars.append(node.attrib['id'])

        matched_chars = {}
        for c in films[id].chars:
            char = films[id].chars[c]
            char = char.lower().split()
            char = map((lambda x: re.sub(r'[^a-z0-9\s]+', '', x)), char)
            char = set(char)

            best = None
            best_i = 0
            for sc in script_chars:
                s_char = set(sc.lower().split())
                if len(char.intersection(s_char)) > best_i:
                    best_i = len(char.intersection(s_char))
                    best = sc

            matched_chars[c] = best

        films[id].script_chars = matched_chars


def match_gexf(films):

    path = '../output/'
    files = []
    for film in glob.glob(path + '*.gexf'):
        files.append(film[len(path):])

    for id in films:
        title = films[id].title.replace(' ', '_').replace(':', '_').replace("'", '').lower()
        file = filter((lambda x: x.lower().startswith(title)), files)
        if len(file) == 1:
            films[id].gexf = file[0]
        elif title.startswith('the'):
            file = filter((lambda x: x.lower().startswith(title[4:])), files)
            assert len(file) == 1
            films[id].gexf = file[0]
        else:
            print title, file
            raise


def construct_films():

    path = '../../experiment/genres/'
    personas = pickle.load(open(path + 'personas.pickle', 'rb'))
    films_ids = {}
    with open(path + 'filtered.meta.data', 'r') as f:
        for row in f:
            id, fb, title = row.split()[0], row.split()[1], row.split()[2:]
            title = ' '.join(title)
            films_ids[id] = (fb, title)

    # dictionoary of dictionaries between films and character fb/names
    chars = defaultdict(lambda: dict())
    with open(path + 'filtered.char.metadata') as f:
        for r in f:
            row = r[:-1].split('\t')
            if row[3]:
                # if character name is known
                for i in [2, 3]:
                    # associate it with both the char FB id and the char-actor map FB id
                    if row[-i]:
                        chars[row[0]][row[-i]] = row[3]

    films = {}
    for id in films_ids:
        title = films_ids[id][1]
        films[id] = Film(id=id,
                         title=title,
                         fb=films_ids[id][0],
                         personas=personas[id],
                         chars=chars[id])

    match_gexf(films)
    match_char_names(films)
    return films