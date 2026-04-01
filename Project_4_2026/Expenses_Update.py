import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

# Configuration
FILE_NAME = "expenses.csv"

def initialize_df():
    """Ensures a CSV exists with the correct columns."""
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    else:
        columns = ["Date", "Category", "Description", "Amount"]
        df = pd.DataFrame(columns=columns)
        df.to_csv(FILE_NAME, index=False)
        return df

def save_sorted(df):
    """Sorts by Amount before saving (Requirement #3)."""
    df = df.sort_values(by="Amount")
    df.to_csv(FILE_NAME, index=False)

def add_expense(category, description, amount):
    """Adds a new expense."""
    df = pd.read_csv(FILE_NAME)

    new_entry = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Category": category,
        "Description": description,
        "Amount": float(amount)
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    save_sorted(df)
    print("\n✅ Expense added successfully!")

def view_summary():
    """Displays all expenses with total + average."""
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("\n📭 No expenses recorded yet.")
        return

    print("\n--- Current Expenses ---")
    print(df)

    total = df["Amount"].sum()
    average = df["Amount"].mean()

    print(f"\n💰 Total Spent: ${total:.2f}")
    print(f"📊 Average Expense: ${average:.2f}")  # Requirement #4

    print("\n--- Spending by Category ---")
    print(df.groupby("Category")["Amount"].sum())

def delete_expense():
    """Deletes an expense by index (Requirement #2)."""
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("\n📭 No expenses to delete.")
        return

    print(df)
    try:
        loc = int(input("Enter index to delete: "))
        df = df.drop(index=loc).reset_index(drop=True)
        save_sorted(df)
        print("🗑️ Expense deleted.")
    except:
        print("Invalid index.")

def edit_expense(): #Added Function - 
    """Edits an existing expense (Requirement #1)."""
    df = pd.read_csv(FILE_NAME) #Pulls the CSV file and reads the data

    if df.empty: #Reads the line to be sure there is data to edit 
        print("\n📭 No expenses to edit.")
        return

    print(df) #Gives error if there is no line

    try: #If there is something to edit
        loc = int(input("Enter index to edit: "))

        new_cat = input("New Category: ") #Option for editing input
        new_desc = input("New Description: ") #Option for new description
        new_amt = float(input("New Amount: ")) #Option for editing a new amount

        # Update row
        df.loc[loc, "Category"] = new_cat #This line rewrites the category - Save Over df looks through data frame
        df.loc[loc, "Description"] = new_desc #This line rewrites the description - loc locates the data in CSV 'dsf'
        df.loc[loc, "Amount"] = new_amt #new_amt rewrites the input 'new_' saves over the data submission 

        # Update timestamp automatically
        df.loc[loc, "Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Using the functions above, datetime / strftime logs the input time

        save_sorted(df)
        print("✏️ Expense updated successfully!")

    except:
        print("Invalid input.")

def plot_expenses():
    """Generates pie chart (Requirement #5)."""
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("\n📭 No data to plot.")
        return

    category_totals = df.groupby('Category')['Amount'].sum()

    plt.figure(figsize=(8, 8))
    plt.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%')
    plt.title('Total Expense by Category')
    plt.axis('equal')
    plt.show()

def main():
    initialize_df()

    while True:
        print("\n--- 📈 Expense Tracker CLI ---")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Delete Expense")
        print("4. Edit Expense")
        print("5. Plot Expenses")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            cat = input("Enter Category: ")
            desc = input("Description: ")
            amt = input("Amount: ")
            add_expense(cat, desc, amt)

        elif choice == "2":
            view_summary()

        elif choice == "3":
            delete_expense()

        elif choice == "4":
            edit_expense()

        elif choice == "5":
            plot_expenses()

        elif choice == "6":
            print("$$ See you next time $$")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main() 