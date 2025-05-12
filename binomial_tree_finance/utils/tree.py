class Node:
    def __init__(self, price=None, option_price=None, parent=None):
        self.price = price
        self.option_price = option_price
        self.parent = parent
        self.children = []
        if parent is not None:
            self.parent.set_child(self)

    def set_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"price:{self.price}, option_price:{self.option_price}"

    def max_depth(self):
        if self.children is None or len(self.children) == 0:
            return 0

        return 1 + max([c.max_depth() for c in self.children])

if __name__ == '__main__':
    root = Node(price=50, option_price=7.43)
    b = Node(price=67.49, option_price=0.93, parent=root)
    c = Node(price=37.04, option_price=14.96, parent=root)

    d = Node(price=91.11, option_price=0, parent=c)
    e = Node(price=50, option_price=2, parent=c)

    f = Node(price=50, option_price=2, parent=d)
    g = Node(price=27.44, option_price=2, parent=d)
    h = Node(price=27.44, option_price=2, parent=g)
    i = Node(price=27.44, option_price=2, parent=h)
    j = Node(price=27.44, option_price=2, parent=i)
    k = Node(price=27.44, option_price=2, parent=root)
    l = Node(price=27.44, option_price=2, parent=d)
    m = Node(price=27.44, option_price=2, parent=h)
    n = Node(price=27.44, option_price=2, parent=m)
    o = Node(price=27.44, option_price=2, parent=n)

    print(root.children)

    print(root.max_depth())