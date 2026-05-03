class Task:
    def __init__(self, name, amount, date, status):
        self.name = name
        self.amount = amount
        self.date = date
        self.status = status


class Obligation(Task):
    pass


class Wishlist(Task):
    def __init__(self, name, amount, date, status, link):
        super().__init__(name, amount, date, status)
        self.link = link