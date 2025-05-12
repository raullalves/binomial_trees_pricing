from binomial_tree_finance.options.equity import EquityPut


def calculate(underlying_type, option_side, **kwargs):
    if underlying_type != 'equity':
        raise Exception("Not Yet Implemented")

    if option_side == 'put':
        return EquityPut(**kwargs).calculate()

if __name__ == '__main__':
    res = calculate(underlying_type='equity',
                    option_type='binomial_american',
                    option_side='put',
                    price=50,
                    vol=0.3,
                    rate=0.05,
                    time_to_expire=2,
                    exercise_price=52,
                    number_of_steps=2)

    print(res)