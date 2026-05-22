import sqlite3
import pandas as pd


#Export των exchanges σε Excel
def export_exchanges_to_excel(filename="exchanges.xlsx"):

    conn = sqlite3.connect("wallet_app.db")

    df = pd.read_sql_query(
        "SELECT * FROM exchanges",
        conn
    )

    conn.close()

    df.to_excel(filename, index=False)


#Export των tasks σε Excel
def export_tasks_to_excel(filename="tasks.xlsx"):

    conn = sqlite3.connect("wallet_app.db")

    df = pd.read_sql_query(
        "SELECT * FROM tasks",
        conn
    )

    conn.close()

    df.to_excel(filename, index=False)