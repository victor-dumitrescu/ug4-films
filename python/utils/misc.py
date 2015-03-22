class TopScores:

    def __init__(self, init_value, max_items=50, order_max=True):
        self.init_value = init_value
        self.max_items = max_items
        self.order_max = order_max
        self.items = [(init_value, None)]

    def get_min(self):
        return min(self.items, key=lambda x: x[0])[0]

    def get_max(self):
        return max(self.items, key=lambda x: x[0])[0]

    def score(self, value, item):

        if self.order_max:
            if value > self.get_min():
                if len(self.items) >= self.max_items:
                    self.items.remove(min(self.items))
                self.items.append((value, item))
        else:
            if value < self.get_max():
                if len(self.items) >= self.max_items:
                    self.items.remove(max(self.items))
                self.items.append((value, item))

    def get_sorted(self):
        return sorted(self.items, key=lambda x: x[0], reverse=True)


def export_to_arff(data, labels, config):

    n_topics = len(data[0] - 1) / 6
    with open('/home/victor/GitHub/experiment/weka/data.arff', 'w') as f:
        f.write('% Configuration: ' + str(config) + '\n')
        f.write('@RELATION personas\n\n')
        for char in range(2):
            for role in config[2]:
                for i in range(n_topics):
                    f.write('@ATTRIBUTE CHR%d_%s%d NUMERIC\n' % (char, role, i))
        f.write('@ATTRIBUTE weight  NUMERIC\n')
        f.write('@ATTRIBUTE class   NUMERIC\n\n\n')

        f.write('@DATA\n\n')
        for i, vector in enumerate(data):
            f.write('%s\n' % ','.join(map(lambda a: '{0:.2f}'.format(a), vector) + [str(labels[i])]))



