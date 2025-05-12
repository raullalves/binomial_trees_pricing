from binomial_tree_finance.options.base import Base

class Equity(Base):
    def __init__(self, option_type, price, vol, rate, time_to_expire, exercise_price, number_of_steps):
        super().__init__(number_of_steps=number_of_steps)

        self.option_type = option_type
        self.price = price
        self.vol = vol
        self.rate = rate
        self.time_to_expire = time_to_expire
        self.exercise_price = exercise_price


class EquityPut(Equity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def calculate(self):
        return 1