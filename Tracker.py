import csv
import pandas as pd
from tkinter import *
from tkinter import ttk

root = Tk()

# -------- ADD EXPENSE --------
def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if date == "" or category == "" or amount == "":
        print("Please fill all required fields")
        return

    f = open("expenses.csv", "a")
    f.write(f"{date},{category},{amount},{description}\n")
    f.close()

    date_entry.delete(0, END)
    category_entry.delete(0, END)
    amount_entry.delete(0, END)
    description_entry.delete(0, END)

    load_expenses()
    calculate_total()


# -------- LOAD EXPENSES --------
def load_expenses():
    expense_table.delete(*expense_table.get_children())
    try:
        f = open("expenses.csv", "r")
        for line in f:
            row = line.strip().split(",")
            expense_table.insert("", END, values=row)
        f.close()
    except FileNotFoundError:
        pass


# -------- CALCULATE TOTAL --------
def calculate_total():
    total = 0
    for r in expense_table.get_children():
        total = total + float(expense_table.item(r)["values"][2])
    total_label.config(text="Total Expense: " + str(total))


# -------- DELETE SELECTED ROW --------
def delete_selected():
    selected = expense_table.selection()
    if selected == ():
        return

    expense_table.delete(selected[0])

    f = open("expenses.csv", "w")
    for r in expense_table.get_children():
        v = expense_table.item(r)["values"]
        f.write(v[0] + "," + v[1] + "," + v[2] + "," + v[3] + "\n")
    f.close()

    calculate_total()


# -------- APPLY FILTER (PANDAS + ILOC + TOLIST) --------
def apply_filter():
    try:
        df = pd.read_csv(
            "expenses.csv",
            names=["Date", "Category", "Amount", "Description"]
        )

        cat = filter_category.get()
        dt = filter_date.get()

        if cat != "":
            df = df.query("Category == @cat")

        if dt != "":
            df = df.query("Date == @dt")

        expense_table.delete(*expense_table.get_children())

        for i in range(len(df)):
            expense_table.insert("", END, values=df.iloc[i].tolist())

        calculate_total()

    except FileNotFoundError:
        pass


# -------- GUI --------
root.title("Expense Tracker")
root.geometry("700x750")

Label(root, text="Date (YYYY-MM-DD):").pack()
date_entry = Entry(root)
date_entry.pack()

Label(root, text="Category:").pack()
category_entry = Entry(root)
category_entry.pack()

Label(root, text="Amount:").pack()
amount_entry = Entry(root)
amount_entry.pack()

Label(root, text="Description:").pack()
description_entry = Entry(root)
description_entry.pack()

Button(root, text="Add Expense", command=add_expense).pack(pady=5)
Button(root, text="Delete Selected", command=delete_selected, bg="red", fg="white").pack(pady=5)

# -------- FILTER UI --------
Label(root, text="Filter Category:").pack()
filter_category = Entry(root)
filter_category.pack()

Label(root, text="Filter Date (YYYY-MM-DD):").pack()
filter_date = Entry(root)
filter_date.pack()

Button(root, text="Apply Filter", command=apply_filter).pack(pady=5)
Button(root, text="Clear Filter", command=load_expenses).pack(pady=5)

# -------- TABLE --------
columns = ("Date", "Category", "Amount", "Description")
expense_table = ttk.Treeview(root, columns=columns, show="headings")
expense_table.pack(pady=10)

for col in columns:
    expense_table.heading(col, text=col)
    expense_table.column(col, width=150)

# -------- TOTAL LABEL --------
total_label = Label(root, text="Total Expense: 0", font=("Arial", 12, "bold"))
total_label.pack(pady=10)

# Load existing data
load_expenses()
calculate_total()

root.mainloop()



