from binomial_tree_finance import compute


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
    assert abs(option_price - 7.428) < 1e-3

def test_2():
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

def test_3():
    time_to_expire_yrs = 2
    num_steps = 2
    perc_up = 0.2
    perc_down = 0.2
    risk_free = 0.05
    price = 50
    exercise_price = 52

    option_side = 'put'
    option_type = 'american'

    option_price = compute(price=price, num_steps=num_steps, time_to_expire=time_to_expire_yrs,
                           exercise_price=exercise_price, option_side=option_side, risk_free=risk_free,
                           option_type=option_type, perc_up=perc_up, perc_down=perc_down)
    assert abs(option_price - 5.0894) < 1e-3


def test_4():
    time_to_expire_yrs = 0.5
    num_steps = 2
    perc_up = 0.1
    perc_down = 0.1
    risk_free = 0.12
    price = 20
    exercise_price = 21

    option_side = 'call'
    option_type = 'european'

    option_price = compute(price=price, num_steps=num_steps, time_to_expire=time_to_expire_yrs,
                           exercise_price=exercise_price, option_side=option_side, risk_free=risk_free,
                           option_type=option_type, perc_up=perc_up, perc_down=perc_down)
    assert abs(option_price - 1.2823) < 1e-3


def test_5():
    time_to_expire_yrs = 2
    num_steps = 5
    vol = 0.3
    risk_free = 0.05
    price = 50
    exercise_price = 52

    option_side = 'put'
    option_type = 'american'

    option_price = compute(price=price, vol=vol, num_steps=num_steps, time_to_expire=time_to_expire_yrs,
                           exercise_price=exercise_price, option_side=option_side, risk_free=risk_free,
                           option_type=option_type)
    assert abs(option_price - 7.671) < 1e-3


def test_6():
    #stock index with dividends

    time_to_expire_yrs = 0.5
    num_steps = 2
    vol = 0.2
    risk_free = 0.05
    price = 810
    exercise_price = 800
    dividend_rate = 0.02

    option_side = 'call'
    option_type = 'european'

    option_price = compute(price=price, vol=vol, num_steps=num_steps, time_to_expire=time_to_expire_yrs,
                           exercise_price=exercise_price, option_side=option_side, risk_free=risk_free,
                           option_type=option_type, dividend_rate=dividend_rate)
    assert abs(option_price - 53.931) < 1e-3


def test_7():
    # Future contract

    time_to_expire_yrs = 9/12
    num_steps = 3
    vol = 0.3
    risk_free = 0.05
    price = 31
    exercise_price = 30
    dividend_rate = 0.02

    option_side = 'put'
    option_type = 'american'
    option_price = compute(price=price, vol=vol, num_steps=num_steps, time_to_expire=time_to_expire_yrs,
                           exercise_price=exercise_price, option_side=option_side, risk_free=risk_free,
                           option_type=option_type, dividend_rate=dividend_rate,
                           is_future=True)
    assert abs(option_price - 2.918) < 1e-3

def check_tests():
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
    test_7()


if __name__ == '__main__':
    check_tests()