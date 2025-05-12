class Base:
    def __init__(self, price, number_of_steps, exercise_price, **kwargs):
        self.number_of_steps = number_of_steps
        self.price = price
        self.exercise_price = exercise_price

        self._generate_tree()

    def _generate_tree(self):
        pass

    def calculate(self):
        pass