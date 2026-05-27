class Task:
    def __init__(self, record_id, user_id, task_type, name, amount, date, status):
        self.record_id = record_id
        self.user_id = user_id
        self.task_type = task_type
        self.name = name
        self.amount = amount
        self.date = date
        self.status = status


class Obligation(Task):
    def __init__(self, record_id, user_id, name, amount, date, status):
        super().__init__(record_id, user_id, "obligation", name, amount, date, status)


class Wishlist(Task):
    def __init__(self, record_id, user_id, name, amount, date, status, link):
        super().__init__(record_id, user_id, "wishlist", name, amount, date, status)
        self.link = link