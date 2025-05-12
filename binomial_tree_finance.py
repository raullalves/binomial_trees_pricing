import numpy as np
import numba as nb
def compute_price2(root, p, discount, option_type, exercise_price, option_side):

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


def compute_option_result(price, exercise_price, option_side):
    if option_side == 'put':
        return 0 if price > exercise_price else exercise_price - price

    if option_side == 'call':
        return 0 if price < exercise_price else price - exercise_price

    raise Exception("Option side not supported")


def compute_price(price_arr, option_price_arr, p, discount, option_type, exercise_price,
           option_side):
    for j in range(price_arr.shape[1] - 2, -1, -1):
        for i in range(price_arr.shape[0]-1, -1, -1):
            if i > j:
                continue
            node_left_i = i
            node_left_j = j + 1
            node_right_i = i + 1
            node_right_j = j + 1

            price = price_arr[i, j]
            left_option_price = option_price_arr[node_left_i, node_left_j]
            right_option_price = option_price_arr[node_right_i, node_right_j]
            opt_pricing_eq = discount * (p * left_option_price + (1 - p) * right_option_price)
            option_result = compute_option_result(price=price,
                                                  exercise_price=exercise_price,
                                                  option_side=option_side)

            if option_type == 'european':
                option_price_arr[i, j] = opt_pricing_eq
            else:
                option_price_arr[i, j] = max(opt_pricing_eq, option_result)

    return option_price_arr[0, 0]



def compute(price, num_steps, time_to_expire, exercise_price, option_side, risk_free, option_type, vol=None,
            perc_up=None, perc_down=None, dividend_rate=0, is_future=False):
    """

    :param price: The current price of the asset
    :param vol: The (optional) vol of the asset, at year basis
    :param num_steps: The number of steps to generate the tree
    :param time_to_expire: The time to the option expires, in years
    :param exercise_price: The option exercise price
    :param option_side: The option side (put or call)
    :param risk_free: The risk-free rate
    :param option_type: The option type (european or american)
    :param perc_up: The optional perc of the asset goes up (in case of not acquired via vol)
    :param perc_down: The optional perc of the asset goes down (in case of not acquired via vol)
    :param dividend_rate: In case the asset has dividends... This is its dividend rate
    :param is_future: In case it's a future contract, there is no discount
    :return:
    """

    dt = time_to_expire/num_steps
    if vol is not None:
        price_factor_neg = np.exp(-vol*np.sqrt(dt))
        price_factor_pos = 1/price_factor_neg
    else:
        price_factor_pos = perc_up + 1
        price_factor_neg = 1-perc_down


    price_arr = np.ones(shape=(num_steps+1, num_steps+1), dtype="float32")
    for j in range(1, price_arr.shape[1]):
        price_arr[:][j] = price_factor_neg**j
    powers_pos = np.arange(num_steps+1, dtype="float32")
    powers_pos = abs(powers_pos - powers_pos[:, None])
    price_arr = np.multiply(price_arr, price_factor_pos**powers_pos)
    price_arr *= price

    discount = np.exp((-risk_free+dividend_rate) * dt) if not is_future else 1
    p = (1/discount - price_factor_neg) / (price_factor_pos - price_factor_neg)

    option_price_arr = np.zeros(shape=(num_steps+1, num_steps+1), dtype="float32")
    option_price_arr[:, -1] = np.vectorize(lambda x: compute_option_result(price=x,
                                                                           exercise_price=exercise_price,
                                                                           option_side=option_side))(price_arr[:, -1])

    opt_price = compute_price(price_arr=price_arr, option_price_arr=option_price_arr, p=p, discount=discount, option_type=option_type, exercise_price=exercise_price,
                  option_side=option_side)

    return opt_price

if __name__ == '__main__':
    time_to_expire_yrs = 2
    num_steps = 2
    perc_up = 0.2
    perc_down = 0.2
    risk_free = 0.05
    price = 50
    exercise_price = 52

    option_side = 'put'
    option_type = 'european'

    option_price = compute(price=price, num_steps=num_steps, time_to_expire=time_to_expire_yrs,
                           exercise_price=exercise_price, option_side=option_side, risk_free=risk_free,
                           option_type=option_type, perc_up=perc_up, perc_down=perc_down)
    assert abs(option_price - 4.1923) < 1e-3