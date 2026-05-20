#Δημιουργούμε base class για obligations και wishlist
class Task:
    def __init__(
        self,
        user_id,
        task_type,
        name,
        amount,
        date,
        status,
        link=None
    
    ):

        self.user_id = user_id
        self.task_type = task_type
        self.name = name
        self.amount = amount 
        self.date = date
        self.status = status
        self.link = link

#Υποκλάση obligation 
class Obligation (Task):
    pass

#Υποκλάση wishlist
class Wishlist(Task):
    pass