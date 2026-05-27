#η κλάση Exchange είναι υπερκλάση των Revenue & Exchange
class Exchange:
    def __init__(self,record_id,user_id,exchange_type,amount,date,category,description):
        self.record_id = record_id
        self.user_id = user_id
        self.exchange_type = exchange_type
        self.amount = amount
        self.date = date
        self.category = category
        self.description = description

class Revenue(Exchange):
    def __init__(self,record_id,user_id, amount,date,category,description):
        super().__init__(record_id, user_id, "revenue",amount,date,category,description)

class Expense(Exchange):
    def __init__(self,record_id,user_id,amount,date,category, description):
        super().__init__(record_id,user_id,"expense",amount,date,category,description)
