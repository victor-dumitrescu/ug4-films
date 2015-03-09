class TopScores:

    def __init__(self, init_value, max_items=10, order_max=True):
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

