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

def traverse_populate(price, vol, num_steps, time_to_expire, exercise_price, option_side, price_factor_neg,
                      price_factor_pos):
    root = Node(price=price)
    curr_level = [root]
    curr_step = 0
    while curr_level:
        next_level = []
        for node in curr_level:
            node.right = Node(node.price*price_factor_neg)
            node.left = Node(node.price*price_factor_pos)
            next_level.append(node.left)
            next_level.append(node.right)

        curr_step += 1
        if curr_step >= num_steps:
            _update_option_price(nodes=[n.left for n in curr_level] + [n.right for n in curr_level], exercise_price=exercise_price, option_side=option_side)
            break
        curr_level = next_level

    return root

def compute_price(root, p, discount, option_type, exercise_price, option_side):

    if root:
        compute_price(root.left, p=p, discount=discount, option_type=option_type, exercise_price=exercise_price,
                      option_side=option_side)
        compute_price(root.right, p=p, discount=discount, option_type=option_type, exercise_price=exercise_price,
                      option_side=option_side)
        if root.option_price is None:
            opt_pricing_eq = discount * (p * root.left.option_price + (1-p) * root.right.option_price)
            option_result = compute_option_price_given_option_side(price=root.price,
                                                                   exercise_price=exercise_price,
                                                                   option_side=option_side)
            if option_type == 'european':
                root.option_price = opt_pricing_eq
            else:
                root.option_price = max(opt_pricing_eq, option_result)

def compute(price, num_steps, time_to_expire, exercise_price, option_side, risk_free, option_type, vol=None,
            perc_up=None, perc_down=None):
    """

    :param price:
    :param vol:
    :param num_steps:
    :param time_to_expire:
    :param exercise_price:
    :param option_side:
    :param risk_free:
    :param option_type:
    :param use_vol:
    :param perc_up:
    :param perc_down:
    :return:
    """

    dt = time_to_expire/num_steps
    if vol is not None:
        price_factor_neg = np.exp(-vol*np.sqrt(dt))
        price_factor_pos = 1/price_factor_neg
    else:
        price_factor_pos = perc_up + 1
        price_factor_neg = 1-perc_down

    root = traverse_populate(price=price, vol=vol, num_steps=num_steps, time_to_expire=time_to_expire,
                             exercise_price=exercise_price, option_side=option_side,
                             price_factor_neg=price_factor_neg, price_factor_pos=price_factor_pos)

    discount = np.exp(-risk_free * dt)
    p = (1/discount - price_factor_neg) / (price_factor_pos - price_factor_neg)
    compute_price(root, p=p, discount=discount, option_type=option_type, exercise_price=exercise_price,
                  option_side=option_side)

    return root.option_price

if __name__ == '__main__':
    time_to_expire_yrs = 2
    num_steps = 2
    vol = 0.3
    risk_free = 0.05
    price = 50
    exercise_price = 52

    option_side = 'put'
    option_type = 'american'

    option_price = compute(price=price, vol=vol, num_steps=num_steps, time_to_expire=time_to_expire_yrs,
                           exercise_price=exercise_price, option_side=option_side, risk_free=risk_free,
                           option_type=option_type)
    print(option_price)