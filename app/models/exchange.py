class Exchange:
    def __init__(self, name, amount, date):
        self.name = name
        self.amount = amount
        self.date = date

class Revenue(Exchange):
    def __init__(self, name, amount, date):
        super().__init__(name, amount, date)


class Expense(Exchange):
    def __init__(self, name, amount, date):
        super().__init__(name, amount, date)




