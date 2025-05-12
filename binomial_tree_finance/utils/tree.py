import numpy as np


class Node:
    def __init__(self, price=None, option_price=None):
        self.price = price
        self.option_price = option_price
        self.left = None
        self.right=None

def compute_option_price_given_option_type(price, exercise_price, option_type):
    if option_type == 'put':
        return 0 if price > exercise_price else exercise_price - price

    raise Exception(f"option type {option_type} not implemented")
def _update_option_price(nodes, exercise_price, option_type):
    for node in nodes:
        node.option_price = compute_option_price_given_option_type(price=node.price,
                                                                   exercise_price=exercise_price,
                                                                   option_type=option_type)
        print(f"Option price is {node.option_price} for price {node.price}")
    return nodes

def traverse_populate(price, vol, num_steps, time_to_expire, exercise_price, option_type):
    root = Node(price=price)
    curr_level = [root]
    curr_step = 1
    dt = time_to_expire/num_steps
    price_factor_neg = np.exp(-vol*np.sqrt(dt))
    price_factor_pos = 1/price_factor_neg
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
            _update_option_price(nodes=[n.left for n in curr_level] + [n.right for n in curr_level], exercise_price=exercise_price, option_type=option_type)
            break
        curr_level = next_level

if __name__ == '__main__':
    traverse_populate(price=50, vol=0.3, num_steps=2, time_to_expire=2, exercise_price=52, option_type='put')