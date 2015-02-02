import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from films import Film, construct_films

TOPICS = {}
with open('../../experiment/genres/topics.csv') as f:
    for r in f:
        row = r.replace('\n', '').split(', ')
        TOPICS[int(row[0])] = row[1:]


def draw_graph(g):

    plt.figure()
    nx.drawing.nx_pylab.draw_networkx(g)
    plt.show()


def get_persona(film, fbs):

    persona = None
    for fb in fbs:
        if fb in film.personas.keys():
            persona = film.personas[fb]
            break

    return persona


def filter_nodes(self, number=None, min_score=None):

    measure = nx.degree_centrality(self)  # dictionary of nodes couples with their centrality
    ranked = sorted(measure.items(), key=lambda x: x[1], reverse=True)
    for r, n in enumerate(ranked[:number]):
        self.add_node(n[0], rank=r+1, value=measure[n[0]])

    assert not (number and min_score)
    if number:
        for n in ranked[number:]:
            self.remove_node(n[0])
    elif min_score:
        pass


def filter_by_persona(self):

    nodes = self.nodes()
    for n in nodes:
        if 'persona' not in self.node[n].keys():
            self.remove_node(n)


def print_persona(d):

    # FIX: number of top words is hardcoded as 3
    def format(t, w):
        w1, w2, w3 = w
        return '%s (%s %s %s)' % (t, w1, w2, w3)

    if 'persona' in d.keys():
        persona = d['persona']
        topics = persona.get_top_topics(3)
        output = []
        for t in topics:
            output.append(format(t.role[0].upper(), TOPICS[t.topic][:3]))
        return output
    else:
        return ''


def get_graphs():

    setattr(nx.classes.graph.Graph, 'filter_nodes', filter_nodes)
    setattr(nx.classes.graph.Graph, 'filter_by_persona', filter_by_persona)

    path = '../output/'
    films = construct_films()
    graphs = {}

    for f in films:
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

        # char_graph.filter_nodes(number=10)
        # char_graph.filter_by_persona()
        char_graph.graph['title'] = films[f].title

        #     print films[f].title, f
        #     for n in sorted(char_graph.node.items(), key=lambda x: int(x[1]['rank'])):
        #         print "%.2f" % round(n[1]['value'], 2), n[0], print_persona(n[1])
        #     print ''

        graphs[f] = char_graph

    return graphs