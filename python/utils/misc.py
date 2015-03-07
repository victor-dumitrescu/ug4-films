class TopScores:

    def __init__(self, init_value, max_items=10):
        self.init_value = init_value
        self.max_items = max_items
        self.items = [(init_value, None)]

    def get_min(self):
        return min(self.items, key=lambda x: x[0])[0]

    def score(self, value, item):
        if value > self.get_min():
            if len(self.items) >= self.max_items:
                self.items.remove(min(self.items))
            self.items.append((value, item))

    def get_sorted(self):
        return sorted(self.items, key=lambda x: x[0], reverse=True)

