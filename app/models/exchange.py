class Exchange:
    def __init__(self, name, amount, date):
        self.name = name
        self.amount = amount
        self.date = date


class Revenue(Exchange):
    pass


class Expense(Exchange):
    pass