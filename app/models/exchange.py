#Δημιουργούμε base class για revenues και expenses
class Exchange:
    def __init__(
        self,
        user_id,
        exchange_type,
        amount,
        date,
        category,
        description
    ):

       self.user_id = user_id 
       self.exchange_type = exchange_type
       self.amount = amount
       self.date = date
       self.category = category
       self.description = description

#Υποκλάση revenue 
class Revenue(Exchange):
    pass


#Υποκλάση expense 
class Expense(Exchange):
    pass