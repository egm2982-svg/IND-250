import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

FILE_NAME = "expenses.csv"


def initialize_df():
    """Create the CSV file if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])
        df.to_csv(FILE_NAME, index=False)


def save_sorted(df):
    """Sort expenses by Amount before saving."""
    df = df.sort_values(by="Amount")  # smallest → largest
    df.to_csv(FILE_NAME, index=False)


def add_expense(category, description, amount):
    """Add a new expense to the file."""
    df = pd.read_csv(FILE_NAME)

    new_entry = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Category": category,
        "Description": description,
        "Amount": float(amount)
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    save_sorted(df)
    print("✅ Expense added!")


def view_summary():
    """Show all expenses + total + category breakdown."""
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("No data yet.")
        return

    print("\nAll Expenses:")
    print(df)

    print("\nTotal Spent:", df["Amount"].sum())
    print("\nBy Category:")
    print(df.groupby("Category")["Amount"].sum())


def show_average():
    """Show the average expense."""
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("No data yet.")
        return

    avg = df["Amount"].mean()
    print(f"\nAverage Expense: ${avg:.2f}")


def top_three_expenses():
    """Show the top 3 largest expenses."""
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("No data yet.")
        return

    top3 = df.sort_values(by="Amount", ascending=False).head(3)
    print("\nTop 3 Expenses:")
    print(top3)


def delete_expense():
    """Delete an expense by index."""
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("No data to delete.")
        return

    print(df)

    try:
        index = int(input("Enter index to delete: "))
        df = df.drop(index=index).reset_index(drop=True)
        save_sorted(df)
        print("Deleted.")
    except:
        print("Invalid input.")


def edit_expense():
    """Edit an existing expense and update timestamp."""
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("No data to edit.")
        return

    print(df)

    try:
        index = int(input("Enter index to edit: "))

        df.loc[index, "Category"] = input("New Category: ")
        df.loc[index, "Description"] = input("New Description: ")
        df.loc[index, "Amount"] = float(input("New Amount: "))

        # update date automatically
        df.loc[index, "Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        save_sorted(df)
        print("Updated.")
    except:
        print("Invalid input.")


def plot_expenses():
    """Create a pie chart of expenses by category."""
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("No data to plot.")
        return

    totals = df.groupby("Category")["Amount"].sum()

    plt.figure()
    plt.pie(totals, labels=totals.index, autopct="%1.1f%%")
    plt.title("Expenses by Category")
    plt.show()


def main():
    """Main menu loop."""
    initialize_df()

    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Delete Expense")
        print("4. Edit Expense")
        print("5. Plot Expenses")
        print("6. Top 3 Expenses")
        print("7. Average Expense")
        print("8. Exit")

        choice = input("Choice: ")

        if choice == "1":
            add_expense(
                input("Category: "),
                input("Description: "),
                input("Amount: ")
            )

        elif choice == "2":
            view_summary()

        elif choice == "3":
            delete_expense()

        elif choice == "4":
            edit_expense()

        elif choice == "5":
            plot_expenses()

        elif choice == "6":
            top_three_expenses()

        elif choice == "7":
            show_average()

        elif choice == "8":
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()