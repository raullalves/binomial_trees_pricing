import numpy as np


class Node:
    def __init__(self, price=None, option_price=None):
        self.price = price
        self.option_price = option_price
        self.left = None
        self.right=None

def compute_option_price_given_option_side(price, exercise_price, option_side):
    if option_side == 'put':
        return 0 if price > exercise_price else exercise_price - price

    if option_side == 'call':
        return 0 if price < exercise_price else price - exercise_price

    raise Exception(f"option type {option_type} not implemented")
def _update_option_price(nodes, exercise_price, option_side):
    for node in nodes:
        node.option_price = compute_option_price_given_option_side(price=node.price,
                                                                   exercise_price=exercise_price,
                                                                   option_side=option_side)
        print(f"Option price is {node.option_price} for price {node.price}")

def traverse_populate(price, vol, num_steps, time_to_expire, exercise_price, option_side):
    root = Node(price=price)
    curr_level = [root]
    curr_step = 1
    dt = time_to_expire/num_steps
    #price_factor_neg = np.exp(-vol*np.sqrt(dt))
    #price_factor_pos = 1/price_factor_neg
    price_factor_neg = 1-vol
    price_factor_pos = (1+vol)
    while curr_level:
        next_level = []
        for node in curr_level:
            node.right = Node(node.price*price_factor_neg)
            node.left = Node(node.price*price_factor_pos)
            next_level.append(node.left)
            next_level.append(node.right)

            print(f"Left has price {node.left.price}")
            print(f"Right has price {node.right.price}")
        curr_step += 1
        print(f"im at step {curr_step}")
        if curr_step > num_steps:
            _update_option_price(nodes=[n.left for n in curr_level] + [n.right for n in curr_level], exercise_price=exercise_price, option_side=option_side)
            break
        curr_level = next_level

    return root

def compute_price(root, p, discount, option_type, exercise_price, option_side):

    if root:

        # First recur on left child
        compute_price(root.left, p=p, discount=discount, option_type=option_type, exercise_price=exercise_price,
                      option_side=option_side)

        # the recur on right child
        compute_price(root.right, p=p, discount=discount, option_type=option_type, exercise_price=exercise_price,
                      option_side=option_side)

        # now print the data of node
        if root.option_price is None:
            opt_pricing_eq = discount * (p * root.left.option_price + (1-p) * root.right.option_price)
            option_result = compute_option_price_given_option_side(price=root.price,
                                                                   exercise_price=exercise_price,
                                                                   option_side=option_side)
            if option_type == 'european':
                root.option_price = opt_pricing_eq
            else:
                root.option_price = max(opt_pricing_eq, option_result)

            print(f"Option price {root.option_price} for price {root.price}")

if __name__ == '__main__':
    time_to_expire = 2
    num_steps = 2
    vol = 0.3
    risk_free = 0.05
    price = 50
    exercise_price = 52
    option_side = 'put'
    option_type = 'american'

    #traverse_populate(price=50, vol=0.3, num_steps=2, time_to_expire=2, exercise_price=52, option_type='put')
    root = traverse_populate(price=price, vol=vol, num_steps=time_to_expire, time_to_expire=num_steps, exercise_price=exercise_price, option_side=option_side)
    dt = time_to_expire/num_steps
    #price_factor_neg = np.exp(-vol*np.sqrt(dt))
    #price_factor_pos = 1/price_factor_neg
    price_factor_neg = 1-vol
    price_factor_pos = (1+vol)
    discount = np.exp(-risk_free * dt)
    p = (1/discount - price_factor_neg) / (price_factor_pos - price_factor_neg)
    compute_price(root, p=p, discount=discount, option_type=option_type, exercise_price=exercise_price,
                  option_side=option_side)

    print(root.option_price)