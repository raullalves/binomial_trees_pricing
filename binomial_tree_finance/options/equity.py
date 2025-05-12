from binomial_tree_finance.options.base import Base

class Equity(Base):
    def __init__(self, option_type, vol, rate, time_to_expire, **kwargs):
        super().__init__(**kwargs)

        self.option_type = option_type
        self.vol = vol
        self.rate = rate
        self.time_to_expire = time_to_expire


class EquityPut(Equity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def calculate(self):
        return 1