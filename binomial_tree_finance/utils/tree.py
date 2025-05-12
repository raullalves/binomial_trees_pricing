import numpy as np


class Node:
    def __init__(self, price=None, option_price=None):
        self.price = price
        self.option_price = option_price
        self.left = None
        self.right=None

def traverse(rootnode):
  thislevel = [rootnode]
  my_level = 0
  while thislevel:
    nextlevel = list()
    print(f"Level {my_level}")
    for n in thislevel:
      print(n.value)
      if n.left: nextlevel.append(n.left)
      if n.right: nextlevel.append(n.right)

    my_level += 1
    thislevel = nextlevel

def traverse_populate(price, vol, num_steps, time_to_expire):
    root = Node(price=price)
    curr_level = [root]
    curr_step = 1
    dt = time_to_expire/num_steps
    price_factor_neg = np.exp(-vol*np.sqrt(dt))
    price_factor_pos = np.exp(vol*np.sqrt(dt))
    while curr_level:
        next_level = []
        for node in curr_level:
            node.left = Node(node.price*price_factor_neg)
            node.right = Node(node.price*price_factor_pos)
            next_level.append(node.left)
            next_level.append(node.right)

            print(f"Left has price {node.left.price}")
            print(f"Right has price {node.right.price}")
        curr_step += 1
        print(f"im at step {curr_step}")
        if curr_step > num_steps:
            break
        curr_level = next_level

if __name__ == '__main__':
    traverse_populate(price=50, vol=0.3, num_steps=2, time_to_expire=2)