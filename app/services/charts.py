import matplotlib.pyplot as plt


#Γράφημα για συνολικά έσοδα και έξοδα
def revenue_expense_chart(total_revenue, total_expense):

    labels = ["Revenue", "Expense"]

    values = [total_revenue, total_expense]

    plt.bar(labels, values)

    plt.title("Revenue vs Expense")

    plt.ylabel("Amount (€)")

    plt.show()


#Γράφημα εξόδων ανά κατηγορία
def expenses_category_chart(expenses_by_category):

    expenses_by_category.plot(kind="bar")

    plt.title("Expenses by Category")

    plt.ylabel("Amount (€)")

    plt.show()