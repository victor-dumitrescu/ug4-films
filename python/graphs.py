import networkx as nx
from collections import defaultdict
from films import Film, construct_films


def get_persona(film, fbs):

    persona = None
    for fb in fbs:
        if fb in film.personas.keys():
            persona = film.personas[fb]
            break

    return persona


def filter_nodes(self, number=None, min_score=None):

    measure = nx.degree_centrality(self)
    ranked = sorted(measure.items(), key=lambda x: x[1], reverse=True)

    if number:
        for n in ranked[number:]:
            self.remove_node(n[0])


def main():

    setattr(nx.classes.graph.Graph, 'filter_nodes', filter_nodes)

    path = '../output/'
    films = construct_films()
    graphs = {}

    for f in films:
        if True:  # f == '30006':
            reverse_script_chars = defaultdict(list)
            for (fb, name) in films[f].script_chars.items():
                if name:
                    reverse_script_chars[name].append(fb)
            # reverse_script_chars = dict(reverse_script_chars)

            char_graph = nx.read_gexf(path + films[f].gexf).to_undirected(reciprocal=True)
            for n in char_graph.node:
                persona = get_persona(films[f], reverse_script_chars[n])
                if persona:
                    char_graph.node[n]['persona'] = persona

            char_graph.filter_nodes(10)
            for n in char_graph.node:
                print n, char_graph.node[n]


main()