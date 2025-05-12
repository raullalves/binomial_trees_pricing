from binomial_tree_finance import compute
import numpy as np


def test_1():
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
    assert np.round(option_price - 7.43) < 1e-5


def check_tests():
    test_1()


if __name__ == '__main__':
    check_tests()