#Αρχείο για convert db rows σε objects
from app.models.exchange import Revenue, Expense
from app.models.task import Obligation, Wishlist

def build_exchange_object(row):
    record_id,user_id,exchange_type,amount,date,category,description = row
    if exchange_type == "revenue":
        return Revenue(record_id,user_id,amount,date,category,description)
    elif exchange_type == "expense":
        return Expense(record_id,user_id,amount,date,category,description)
    else:
        raise ValueError(f"Unknown exchange_type: {exchange_type}")

def build_task_object(row):
    record_id,user_id,task_type,name,amount,date,status,link = row
    if task_type == "obligation":
        return Obligation(record_id,user_id,name,amount,date,status)
    elif task_type == "wishlist":
        return Wishlist(record_id, user_id,name,amount,date,status,link)
    else:
        raise ValueError(f"Unknown task_type: {task_type}")
