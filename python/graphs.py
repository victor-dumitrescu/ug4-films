import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from films import Film, construct_films

TOPICS = {}
with open('/home/victor/GitHub/experiment/genres/topics.csv') as f:
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
    # prunes the graph of nodes which don't have a certain rank/centrality)

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
    # removes nodes which don't have a persona

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


def get_graphs(verbose=False, **kwargs):

    filter_top = kwargs.get('filter_nodes', False)
    filter_persona = kwargs.get('filter_persona', False)

    setattr(nx.classes.graph.Graph, 'filter_nodes', filter_nodes)
    setattr(nx.classes.graph.Graph, 'filter_by_persona', filter_by_persona)

    path = '/home/victor/GitHub/ug4-films/output/'
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

        # I really need a better system for this. Comment out next lines if doing linear regression.
        if filter_top:
            char_graph.filter_nodes(number=filter_top)
        if filter_persona:
            char_graph.filter_by_persona()

        char_graph.graph['title'] = films[f].title
        char_graph.graph['gexf'] = films[f].gexf

        if verbose:
            print films[f].title, f
            for n in sorted(char_graph.node.items(), key=lambda x: int(x[1]['rank'])):
                print "%.2f" % round(n[1]['value'], 2), n[0], print_persona(n[1])
            print ''

        graphs[f] = char_graph

    return graphs