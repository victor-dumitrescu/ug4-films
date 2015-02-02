from graphs import get_graphs

graphs = get_graphs()
graphs['30006'].filter_by_persona()

#TODO Construct the feature vectors: persona distributions + edge weight
#TODO Get labels: total sentiment from one person to the other